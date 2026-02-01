"""
搜索工具实现
使用 DuckDuckGo 搜索 - 免费无需 API Key
"""

import httpx
from typing import List
import re


class SearchResult:
    """搜索结果数据结构"""
    def __init__(self, title: str, url: str, content: str):
        self.title = title
        self.url = url
        self.content = content
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content
        }
    
    def __str__(self) -> str:
        return f"[{self.title}]({self.url})\n{self.content}"


async def search_with_duckduckgo_html(query: str, num_results: int = 5) -> List[SearchResult]:
    """
    使用 DuckDuckGo HTML 版本进行搜索
    解析 HTML 页面获取搜索结果
    """
    url = "https://html.duckduckgo.com/html/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    data = {
        "q": query,
        "b": "",
        "kl": "cn-zh"  # 中文结果
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        html = response.text
    
    results = []
    
    # 简单的 HTML 解析提取结果
    # 查找结果块
    result_pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
    snippet_pattern = r'<a class="result__snippet"[^>]*>([^<]+(?:<[^>]+>[^<]*</[^>]+>)*[^<]*)</a>'
    
    links = re.findall(result_pattern, html)
    snippets = re.findall(snippet_pattern, html)
    
    for i, (link, title) in enumerate(links[:num_results]):
        # 清理 URL
        if link.startswith("//duckduckgo.com/l/?uddg="):
            # 提取实际 URL
            import urllib.parse
            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
            actual_url = parsed.get("uddg", [link])[0]
            link = urllib.parse.unquote(actual_url)
        
        # 获取对应的摘要
        snippet = snippets[i] if i < len(snippets) else ""
        # 清理 HTML 标签
        snippet = re.sub(r'<[^>]+>', '', snippet)
        
        results.append(SearchResult(
            title=title.strip(),
            url=link,
            content=snippet.strip()
        ))
    
    return results


async def search_with_duckduckgo_api(query: str, num_results: int = 5) -> List[SearchResult]:
    """
    使用 DuckDuckGo Instant Answer API
    适合获取维基百科等结构化信息
    """
    url = "https://api.duckduckgo.com/"
    
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    
    results = []
    
    # 处理 Abstract（摘要）
    if data.get("Abstract"):
        results.append(SearchResult(
            title=data.get("Heading", query),
            url=data.get("AbstractURL", ""),
            content=data.get("Abstract", "")
        ))
    
    # 处理 RelatedTopics
    for topic in data.get("RelatedTopics", []):
        if len(results) >= num_results:
            break
        if isinstance(topic, dict) and "Text" in topic:
            text = topic.get("Text", "")
            results.append(SearchResult(
                title=text[:60] + "..." if len(text) > 60 else text,
                url=topic.get("FirstURL", ""),
                content=text
            ))
    
    return results


async def web_search(query: str, num_results: int = 5) -> str:
    """
    统一的搜索接口
    优先使用 HTML 版本（结果更全），失败则使用 API 版本
    
    返回格式化的搜索结果字符串
    """
    results = []
    search_method = ""
    
    try:
        # 优先使用 HTML 版本
        results = await search_with_duckduckgo_html(query, num_results)
        search_method = "DuckDuckGo"
    except Exception as e:
        print(f"[Search HTML Error]: {e}")
        try:
            # 备用：使用 API 版本
            results = await search_with_duckduckgo_api(query, num_results)
            search_method = "DuckDuckGo API"
        except Exception as e2:
            print(f"[Search API Error]: {e2}")
            return f"搜索失败: {str(e2)}"
    
    if not results:
        return f"未找到关于 '{query}' 的搜索结果"
    
    # 格式化输出
    output_lines = [f"【搜索结果 - {search_method}】\n"]
    
    for i, result in enumerate(results, 1):
        output_lines.append(f"{i}. **{result.title}**")
        if result.url:
            output_lines.append(f"   链接: {result.url}")
        if result.content:
            output_lines.append(f"   摘要: {result.content}\n")
        else:
            output_lines.append("")
    
    return "\n".join(output_lines)


# 工具函数映射
TOOL_FUNCTIONS = {
    "web_search": web_search
}


async def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    执行指定的工具
    
    Args:
        tool_name: 工具名称
        tool_input: 工具参数
    
    Returns:
        工具执行结果
    """
    if tool_name not in TOOL_FUNCTIONS:
        return f"未知工具: {tool_name}"
    
    tool_func = TOOL_FUNCTIONS[tool_name]
    
    # 提取参数
    query = tool_input.get("query", "")
    num_results = tool_input.get("num_results", 5)
    
    # 执行工具
    result = await tool_func(query, num_results)
    
    return result

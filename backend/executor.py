"""
Executor 智能体
负责执行 Planner 产生的子任务列表
"""

import json
import httpx
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from search_tool import execute_tool

# 使用 deepseek-chat 模型执行任务（更快，输出更完整）
EXECUTOR_MODEL = "deepseek-chat"


async def call_deepseek_for_executor(prompt: str, system_prompt: str = None, max_tokens: int = 4096) -> str:
    """
    调用 DeepSeek API 执行任务
    使用 deepseek-chat 模型，设置较大的 max_tokens 确保完整输出
    """
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": EXECUTOR_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json()
        
        # 检查是否因为长度限制被截断
        finish_reason = result.get("choices", [{}])[0].get("finish_reason", "")
        if finish_reason == "length":
            print(f"[Warning] Response was truncated due to max_tokens limit")
        
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"[API Response] finish_reason: {finish_reason}, length: {len(content)} chars")
        return content


async def execute_synthesize_task(
    task_description: str,
    user_query: str,
    previous_results: dict
) -> str:
    """
    执行综合分析任务
    """
    # 构建上下文
    context_parts = []
    for task_id, result in previous_results.items():
        # 限制每个任务结果的长度，避免上下文过长
        truncated_result = result[:3000] if len(result) > 3000 else result
        context_parts.append(f"【任务{task_id}的结果】\n{truncated_result}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    synthesize_prompt = f"""你是一个专业的分析助手。请基于以下信息完成任务。

## 用户原始问题
{user_query}

## 当前任务
{task_description}

## 前置任务的执行结果
{context}

## 输出要求
1. 给出完整、清晰、有条理的回答
2. 使用 Markdown 格式
3. **重要**：保持回答精炼，每个要点用2-3句话概括
4. 如果要使用表格，请确保表格简洁（每列内容不超过30字）
5. 优先使用列表而非大表格
6. 总字数控制在1500字以内

请开始回答：
"""

    # 打印输入给最终模型的内容（用于调试）
    print(f"\n{'='*60}")
    print(f"[Executor] 调用最终模型生成答案")
    print(f"[Executor] 输入内容预览:")
    print(f"用户问题: {user_query[:200]}...")
    print(f"任务描述: {task_description[:200]}...")
    print(f"前置任务结果数量: {len(previous_results)}")
    print(f"上下文总长度: {len(context)} 字符")
    print(f"完整输入提示词长度: {len(synthesize_prompt)} 字符")
    print(f"{'='*60}")

    result = await call_deepseek_for_executor(synthesize_prompt, max_tokens=4096)
    return result


async def execute_subtask(
    task: dict,
    user_query: str,
    previous_results: dict
) -> str:
    """
    执行单个子任务
    
    Args:
        task: 子任务定义
        user_query: 用户原始问题
        previous_results: 前置任务的执行结果
    
    Returns:
        任务执行结果
    """
    task_id = task.get("id")
    task_name = task.get("name", "")
    task_type = task.get("type", "")
    tool = task.get("tool")
    tool_input = task.get("tool_input", {})
    description = task.get("description", "")
    
    result = ""
    
    if task_type == "search" and tool:
        # 搜索类任务，调用工具
        result = await execute_tool(tool, tool_input)
        
        print(f"\n[Tool: {tool}] Query: {tool_input.get('query', '')}")
        print(f"[Tool Result Length]: {len(result)} chars")
        
    elif task_type == "synthesize":
        # 综合类任务
        result = await execute_synthesize_task(description, user_query, previous_results)
        
        print(f"\n[Synthesize Task {task_id}]: {task_name}")
        print(f"[Result Length]: {len(result)} characters")
        
    elif task_type == "analyze":
        # 分析类任务
        analyze_prompt = f"""请完成以下分析任务：

任务：{description}
用户问题：{user_query}

请给出详细但精炼的分析结果，控制在1000字以内。"""
        result = await call_deepseek_for_executor(analyze_prompt, max_tokens=2048)
        
        print(f"\n[Analyze Task {task_id}]: {task_name}")
        print(f"[Result Length]: {len(result)} chars")
    else:
        result = f"未知任务类型: {task_type}"
        print(f"\n[Unknown Task Type]: {task_type}")
    
    return result

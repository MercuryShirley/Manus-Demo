"""
工具列表配置文件
定义模型可以调用的工具及其参数
"""

# 工具列表
TOOLS = [
    {
        "name": "web_search",
        "description": "搜索互联网获取实时信息。当需要查找最新新闻、事实、数据或任何需要联网获取的信息时使用此工具。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索查询关键词"
                },
                "num_results": {
                    "type": "integer",
                    "description": "返回结果数量，默认为5",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
]


def get_tools_description() -> str:
    """
    生成工具列表的文本描述，供提示词使用
    """
    tools_desc = []
    for tool in TOOLS:
        params_desc = []
        props = tool["parameters"].get("properties", {})
        required = tool["parameters"].get("required", [])
        
        for param_name, param_info in props.items():
            is_required = "必填" if param_name in required else "可选"
            default = f"，默认值: {param_info.get('default')}" if "default" in param_info else ""
            params_desc.append(
                f"    - {param_name} ({param_info['type']}, {is_required}): {param_info['description']}{default}"
            )
        
        tools_desc.append(
            f"工具名称: {tool['name']}\n"
            f"工具描述: {tool['description']}\n"
            f"参数:\n" + "\n".join(params_desc)
        )
    
    return "\n\n".join(tools_desc)


def get_tools_for_api() -> list:
    """
    返回适合 API 调用格式的工具列表
    """
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        }
        for tool in TOOLS
    ]

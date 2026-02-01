"""
Verify 智能体
负责校验和优化 Executor 生成的最终回复
"""

import httpx
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

# 使用 deepseek-chat 模型进行校验
VERIFIER_MODEL = "deepseek-chat"


async def verify_and_optimize(
    original_reply: str,
    user_query: str,
    task_results: dict
) -> str:
    """
    校验和优化最终回复
    
    Args:
        original_reply: Executor 生成的原始回复
        user_query: 用户原始问题
        task_results: 所有子任务的执行结果
    
    Returns:
        优化后的回复
    """
    # 构建任务结果摘要（用于上下文）
    task_summary = []
    for task_id, result in task_results.items():
        # 只取前500字符作为摘要
        summary = result[:500] + "..." if len(result) > 500 else result
        task_summary.append(f"任务{task_id}结果摘要: {summary}")
    
    context = "\n".join(task_summary)
    
    verify_prompt = f"""你是一个质量检查助手（Verify Agent）。请校验并优化以下回答。

## 用户原始问题
{user_query}

## 可用的任务执行结果
{context}

## 当前生成的回答
{original_reply}

## 校验和优化要求
1. **完整性检查**：确保回答完整，没有在中途截断
2. **准确性检查**：确保回答准确回答了用户的问题
3. **格式检查**：确保 Markdown 格式正确（表格、列表、标题等）
4. **内容优化**：
   - 如果回答被截断，请补全缺失部分
   - 如果表格不完整，请补全表格
   - 如果内容冗余，请精简表达
   - 确保所有要点都清晰表达
5. **长度控制**：如果回答过长（超过2000字），请适当精简，但保持完整性

## 输出
请直接输出优化后的完整回答，不要添加额外的说明或注释。确保回答完整且格式正确。
"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [
        {"role": "user", "content": verify_prompt}
    ]

    payload = {
        "model": VERIFIER_MODEL,
        "messages": messages,
        "max_tokens": 8192,  # 确保有足够空间输出完整内容
        "temperature": 0.3,  # 较低温度，保持一致性
    }

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json()
        
        finish_reason = result.get("choices", [{}])[0].get("finish_reason", "")
        verified_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        print(f"\n[Verify] finish_reason: {finish_reason}")
        print(f"[Verify] Output length: {len(verified_reply)} characters")
        print(f"[Verify] Output preview:\n{verified_reply[:500]}...")
        
        return verified_reply

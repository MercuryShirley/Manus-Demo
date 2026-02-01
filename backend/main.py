from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import json
import asyncio
import base64

from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL
from prompts import get_planner_prompt
from executor import execute_subtask
from verifier import verify_and_optimize

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    reply: str
    reasoning_content: str | None = None
    plan: dict | None = None


async def call_deepseek(user_message: str, system_prompt: str = None) -> dict:
    """
    Call DeepSeek API with the user's message.
    """
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="DeepSeek API Key not configured. Please set DEEPSEEK_API_KEY in .env file."
        )

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[API Error]: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"DeepSeek API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            print(f"[Request Error]: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to DeepSeek API: {str(e)}"
            )


def parse_planner_response(content: str) -> dict:
    """
    解析 Planner 的 JSON 响应
    """
    try:
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            json_str = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            json_str = content[start:end].strip()
        else:
            json_str = content.strip()
        
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"[JSON Parse Error]: {e}")
        return {
            "query_analysis": "无法解析规划结果",
            "subtasks": [
                {
                    "id": 1,
                    "name": "直接回复",
                    "description": content,
                    "type": "synthesize",
                    "tool": None,
                    "tool_input": {},
                    "depends_on": []
                }
            ]
        }


def send_sse_event(event_type: str, data: dict) -> str:
    """
    发送 SSE 事件，对大型内容进行 base64 编码以避免传输问题
    """
    # 对 reply 字段进行特殊处理
    if 'reply' in data and data['reply']:
        # 使用 base64 编码长文本，避免 JSON 和 SSE 解析问题
        encoded = base64.b64encode(data['reply'].encode('utf-8')).decode('ascii')
        data = {**data, 'reply_base64': encoded}
        del data['reply']
    
    json_str = json.dumps(data, ensure_ascii=False)
    return f"data: {json_str}\n\n"


async def event_generator(user_message: str):
    """
    SSE 事件生成器，用于流式返回处理进度
    """
    print(f"\n{'='*60}")
    print(f"[User Query]: {user_message}")
    print(f"{'='*60}")

    # 阶段1: 发送"规划中"状态
    yield send_sse_event('status', {'type': 'status', 'status': 'planning', 'message': '正在规划任务...'})
    await asyncio.sleep(0.1)

    # 获取 Planner 提示词并调用
    planner_prompt = get_planner_prompt()
    result = await call_deepseek(user_message, system_prompt=planner_prompt)

    # 提取响应内容
    choice = result.get("choices", [{}])[0]
    message = choice.get("message", {})
    content = message.get("content", "")

    # 解析规划结果
    plan = parse_planner_response(content)
    
    # 只打印 Planner 输出
    print(f"\n[Planner Output]:")
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    subtasks = plan.get("subtasks", [])
    
    # 阶段2: 发送任务列表（TODO清单）
    todo_list = []
    for task in subtasks:
        todo_list.append({
            "id": task.get("id"),
            "name": task.get("name"),
            "description": task.get("description"),
            "type": task.get("type"),
            "depends_on": task.get("depends_on", []),
            "status": "pending"
        })
    
    yield send_sse_event('plan', {'type': 'plan', 'query_analysis': plan.get('query_analysis', ''), 'todos': todo_list})
    await asyncio.sleep(0.1)
    
    print(f"\n[Executor] Starting task execution...")

    # 阶段3: 按顺序执行子任务
    task_results = {}
    completed_ids = set()
    
    while len(completed_ids) < len(subtasks):
        executed_any = False
        
        for task in subtasks:
            task_id = task.get("id")
            if task_id in completed_ids:
                continue
            
            # 检查依赖是否满足
            depends_on = task.get("depends_on", [])
            if not all(dep_id in completed_ids for dep_id in depends_on):
                continue
            
            executed_any = True
            
            # 发送任务开始执行的状态
            yield send_sse_event('task_start', {'type': 'task_start', 'task_id': task_id, 'task_name': task.get('name')})
            await asyncio.sleep(0.1)
            
            # 执行任务
            try:
                result = await execute_subtask(task, user_message, task_results)
                task_results[task_id] = result
            except Exception as e:
                print(f"[Task {task_id} Error]: {str(e)}")
                task_results[task_id] = f"任务执行出错: {str(e)}"
            
            completed_ids.add(task_id)
            
            # 发送任务完成状态
            yield send_sse_event('task_complete', {'type': 'task_complete', 'task_id': task_id, 'task_name': task.get('name')})
            await asyncio.sleep(0.1)
            
            break
        
        if not executed_any:
            print("[Warning]: No executable tasks, possible circular dependency")
            break
    
    # 阶段4: 生成最终结果（Executor 生成）
    print(f"\n[Executor] All tasks completed. Generating final response...")
    final_result = ""
    for task in reversed(subtasks):
        if task.get("type") == "synthesize":
            final_result = task_results.get(task.get("id"), "")
            break
    
    if not final_result and task_results:
        final_result = list(task_results.values())[-1]
    
    print(f"\n[Executor] Final response generated. Length: {len(final_result)} characters")
    
    # 阶段5: Verify 智能体验证和优化
    print(f"\n[Verify] Starting verification and optimization...")
    verified_result = await verify_and_optimize(
        original_reply=final_result,
        user_query=user_message,
        task_results=task_results
    )
    
    print(f"\n[Verify] Verification completed. Final output length: {len(verified_result)} characters")
    print(f"{'='*60}\n")
    
    # 发送优化后的最终结果
    yield send_sse_event('final', {'type': 'final', 'reply': verified_result})
    await asyncio.sleep(0.1)
    yield send_sse_event('done', {'type': 'done'})


@app.post("/chat/stream")
async def chat_stream(request: MessageRequest):
    """
    流式聊天接口，使用 SSE 返回实时进度
    """
    return StreamingResponse(
        event_generator(request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """
    非流式聊天接口（保留兼容）
    """
    planner_prompt = get_planner_prompt()
    result = await call_deepseek(request.message, system_prompt=planner_prompt)

    choice = result.get("choices", [{}])[0]
    message = choice.get("message", {})
    content = message.get("content", "")
    reasoning_content = message.get("reasoning_content", None)

    plan = parse_planner_response(content)

    subtasks = plan.get("subtasks", [])
    if len(subtasks) == 1 and subtasks[0].get("type") == "synthesize":
        reply = subtasks[0].get("description", content)
    else:
        lines = [f"📋 {plan.get('query_analysis', '')}"]
        for task in subtasks:
            lines.append(f"⏳ 任务{task.get('id')}: {task.get('name')}")
        reply = "\n".join(lines)

    return MessageResponse(
        reply=reply,
        reasoning_content=reasoning_content,
        plan=plan
    )


@app.get("/")
async def root():
    return {"status": "ok", "message": "Manus Backend is running"}


@app.get("/tools")
async def list_tools():
    from tools import TOOLS
    return {"tools": TOOLS}

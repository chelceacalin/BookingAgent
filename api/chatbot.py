from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

chatbot = APIRouter()


class ChatRequest(BaseModel):
    sessionId: str
    query: str


async def generate_response(sessionId: str, query: str):
    config: RunnableConfig = {"configurable": {"thread_id": sessionId}}
    from agent import agent as agent_module

    async for event in agent_module.graph.astream(
            {"messages": [HumanMessage(content=query)]}, config
    ):
        if "agent" in event:
            message = event["agent"]["messages"][-1]
            if hasattr(message, "tool_calls") and message.tool_calls:
                for tc in message.tool_calls:
                    yield f"data: [Calling tool {tc.get('name')} with args: {tc.get('args')}]\n\n"

            content = message.content if hasattr(message, "content") else None

            if isinstance(content, str) and content:
                safe = content.replace("\n", "\\n")
                yield f"data: {safe}\n\n"

            elif isinstance(content, list) and content:
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text" and block.get("text"):
                        safe = block["text"].replace("\n", "\\n")
                        yield f"data: {safe}\n\n"

        elif "tools" in event:
            tool_msg = event["tools"]["messages"][0]
            if hasattr(tool_msg, "content"):
                yield f"data: [Tool result: {tool_msg.content}]\n\n"
@chatbot.post("/chat")
def chat(body: ChatRequest):
    sessionId = body.sessionId
    query = body.query
    config: RunnableConfig = {"configurable": {"thread_id": sessionId}}
    import agent.agent as agent

    result = agent.graph.invoke({"messages": [HumanMessage(content=query)]}, config)

    messages = result.get("messages", [])
    last_message = messages[-1]

    response_text = ""
    if hasattr(last_message, "content"):
        content = last_message.content
        if isinstance(content, str):
            response_text = content
        else:
            response_text = str(content)
    else:
        response_text = str(last_message)

    return {"response": response_text}


@chatbot.post("/chat/stream")
async def chat_stream(body: ChatRequest):
    return StreamingResponse(
        generate_response(body.sessionId, body.query),
        media_type="text/event-stream",
    )
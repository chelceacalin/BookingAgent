from fastapi import APIRouter
from pydantic import BaseModel

from langchain_core.runnables import RunnableConfig

chatbot = APIRouter()

class ChatRequest(BaseModel):
    sessionId: str
    query: str

@chatbot.post('/chat')
def chat(body: ChatRequest):
    sessionId = body.sessionId
    query = body.query
    config: RunnableConfig = {"configurable": {"thread_id": sessionId}}
    from agent import graph
    result = graph.invoke({"messages": [{"role": "user", "content": query}]}, config)

    messages = result.get("messages", [])
    last_message = messages[-1]

    if hasattr(last_message, 'content'):
        response_text = last_message.content
    else:
        response_text = last_message.get('content', '')

    return {"response": response_text}

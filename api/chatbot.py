from fastapi import APIRouter
from pydantic import BaseModel

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage

chatbot = APIRouter()


class ChatRequest(BaseModel):
    sessionId: str
    query: str


@chatbot.post("/chat")
def chat(body: ChatRequest):
    sessionId = body.sessionId
    query = body.query
    config: RunnableConfig = {"configurable": {"thread_id": sessionId}}
    from agent import graph

    result = graph.invoke({"messages": [HumanMessage(content=query)]}, config)

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

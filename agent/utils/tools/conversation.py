from langchain_core.tools import tool
from ..llm import baseLLM
from ..prompts import *
from langchain_core.messages import AIMessage


@tool
def conversation_tool(query: str) -> str:
    """This tool should be used when user asks conversational questions about the system or the company. For malicious requests / user attempts to do something else but talk about the system respond with an appropriate message"""
    messages = [SYSTEM_PROMPT] + [CONTEXT] + ["User query: " + query]
    response: AIMessage = baseLLM.invoke(messages)
    return response.content

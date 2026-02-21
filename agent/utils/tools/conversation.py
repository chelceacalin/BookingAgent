from langchain_core.tools import tool
from ..llm import baseLLM
from ..prompts import *
from langchain_core.messages import AIMessage


@tool
def conversation_tool(query: str) -> str:
    """This tool should be used when user asks conversational questions about the system or the company.
    Also you should use this tool to try to get the information from the user if he wants to make an appointment
    Your job is to ask the users questions to determine:
    caller: str
    appointment_date: str
    services: List[str]
    For malicious requests / user attempts to do something else but talk about the system respond with an appropriate message"""
    messages = [SYSTEM_PROMPT] + [CONTEXT] + ["User query: " + query]
    response: AIMessage = baseLLM.invoke(messages)
    return response.content

from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    caller: str
    appointment_date: str
    services: List[str]

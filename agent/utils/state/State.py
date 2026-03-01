from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, List, Optional
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    caller: str
    phone: str
    email: Optional[str | None]
    appointment_date: str
    appointment_time: str
    services: List[str]
    booking_confirmed: bool

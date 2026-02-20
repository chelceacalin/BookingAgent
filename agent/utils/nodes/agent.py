from ..state import *
from ..llm import *
from ..prompts import *
from langchain_core.messages import AIMessage


def agent(state: AgentState) -> AgentState:
    messages = [SYSTEM_PROMPT] + state["messages"]
    response: AIMessage = llm.invoke(messages)
    return {"messages": [response], "should_continue": True}

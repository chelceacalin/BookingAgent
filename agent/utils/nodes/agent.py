from ..state import *
from ..llm import *
from langchain_core.messages import AIMessage


def agent(state: AgentState) -> AgentState:
    response: AIMessage = llm.invoke(state["messages"])
    return {"messages": [response]}

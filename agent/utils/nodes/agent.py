from ..state import *
from ..llm import *
from ..prompts import *
from langchain_core.messages import AIMessage, SystemMessage


def agent(state: AgentState) -> AgentState:
    history = state["messages"][-20:]
    messages = [SystemMessage(content=SYSTEM_PROMPT + CONTEXT)] + history
    response: AIMessage = llm.invoke(messages)
    return {"messages": [response]}

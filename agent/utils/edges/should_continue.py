from ..state import *
from ..llm import *
from ..prompts import *
from langchain_core.messages import AIMessage


def should_continue(agentState: AgentState):
    last_message = agentState["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "end"

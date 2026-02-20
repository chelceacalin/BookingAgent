from langgraph.graph import StateGraph, END, START
from .utils.state import *
from .utils.nodes import *

graph_build = StateGraph(AgentState)  # type: ignore
graph_build.add_node("agent", agent)

graph_build.add_edge(START, "agent")
graph_build.add_edge("agent", END)

graph = graph_build.compile()

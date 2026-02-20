from langgraph.graph import StateGraph, END, START
from .utils.state import *
from .utils.nodes import *
from .utils.edges import *

graph_build = StateGraph(AgentState)  # type: ignore
graph_build.add_node("agent", agent)

graph_build.add_edge(START, "agent")
graph_build.add_conditional_edges("agent", should_continue, {"tools": END, "end": END}
                                  )

graph = graph_build.compile()

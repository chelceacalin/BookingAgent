from langgraph.graph import StateGraph, END, START
from .utils.state import *
from .utils.nodes import *
from .utils.edges import *
from .utils.memory import checkpointer

graph_build = StateGraph(AgentState)  # type: ignore
graph_build.add_node("agent", agent)
graph_build.add_node("tools", tool_node)

graph_build.add_edge(START, "agent")
graph_build.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END}
                                  )
graph_build.add_edge("tools", "agent")
graph = graph_build.compile(
    checkpointer=checkpointer,
)

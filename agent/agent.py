from langgraph.graph import StateGraph, END, START
from .utils.state import *
from .utils.nodes import *
from .utils.edges import *
from .utils.memory.memory import pool
from config.logging_config import logger

graph_build = StateGraph(AgentState)
graph_build.add_node("agent", agent)
graph_build.add_node("tools", tool_node)

graph_build.add_edge(START, "agent")
graph_build.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
graph_build.add_edge("tools", "agent")

graph = None


async def init_graph():
    global graph
    try:
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
        await pool.open()
        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()
        graph = graph_build.compile(checkpointer=checkpointer)
    except Exception as e:
        logger.error(f"init_graph FAILED: {e}", exc_info=True)
        raise
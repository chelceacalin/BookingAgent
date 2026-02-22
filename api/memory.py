from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()
memory = APIRouter()

@memory.get('/{session_id}')
def debug_memory(session_id):
    from agent import graph
    config = {"configurable": {"thread_id": session_id}}
    state = graph.get_state(config)

    if not state or not state.values:
        return JSONResponse(status_code=404, content={"error": "No state found for this session"})

    messages = state.values.get("messages", [])
    serialized = [
        {"role": msg.type, "content": msg.content}
        for msg in messages
    ]
    return JSONResponse(content={"thread_id": session_id, "messages": serialized[-20:]})

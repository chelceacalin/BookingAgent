from flask import Blueprint, jsonify
from dotenv import load_dotenv
load_dotenv()
memory = Blueprint('memory', __name__)

@memory.route('/<session_id>', methods=['GET'])
def debug_memory(session_id):
    from agent import graph
    config = {"configurable": {"thread_id": session_id}}
    state = graph.get_state(config)

    if not state or not state.values:
        return jsonify({"error": "No state found for this session"}), 404

    messages = state.values.get("messages", [])
    serialized = [
        {"role": msg.type, "content": msg.content}
        for msg in messages
    ]
    return jsonify({"thread_id": session_id, "messages": serialized[-20:]})



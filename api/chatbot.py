from flask import Blueprint, request, jsonify
from langchain_core.runnables import RunnableConfig

chatbot = Blueprint('chatbot', __name__)


@chatbot.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    sessionId = data.get('sessionId')
    query = data.get('query')

    if not sessionId or not query:
        return jsonify({"error": "Missing 'sessionId' or 'query'"}), 400

    config: RunnableConfig = {"configurable": {"thread_id": sessionId}}
    from agent import graph
    result = graph.invoke({"messages": [{"role": "user", "content": query}]}, config)

    messages = result.get("messages", [])
    last_message = messages[-1]

    if hasattr(last_message, 'content'):
        response_text = last_message.content
    else:
        response_text = last_message.get('content', '')

    return jsonify({"response": response_text})

from flask import Blueprint,request,jsonify

chatbot = Blueprint('chatbot', __name__)


@chatbot.route('/chat', methods=['POST'])
def chat():
    data = request.json
    return {"response": "hi"}

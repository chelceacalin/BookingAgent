from flask import Flask, request, jsonify
from api import chatbot, memory, server
from .logging_config import logger

app = Flask(__name__)
app.register_blueprint(chatbot)
app.register_blueprint(memory, url_prefix='/memory')
app.register_blueprint(server, url_prefix='/server')


@app.before_request
def before_request():
    if request.path == "/chat" and request.is_json:
        query = request.get_json().get("query", None)
        if query:
            logger.info("Got query: " + str(query))


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    logger.error(e)
    return jsonify(error=str(e)), code


@app.after_request
def after_request(response):
    return response

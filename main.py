from flask import Flask
from api import chatbot

app = Flask(__name__)
app.register_blueprint(chatbot)

@app.route("/", methods=["GET"])
def sayhi():
    return  ""

if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
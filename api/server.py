from flask import Blueprint, Response
from agent import graph

server = Blueprint('server', __name__)

@server.route('/graph', methods=['GET'])
def get_graph_image():
    try:
        graphImage = graph.get_graph().draw_mermaid_png()
        return Response(graphImage, mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 500

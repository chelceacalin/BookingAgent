from fastapi import APIRouter
from fastapi.responses import JSONResponse,Response

server = APIRouter()

@server.get('/graph')
def get_graph_image():
    try:
        from agent import graph
        graph_image = graph.get_graph().draw_mermaid_png()
        return Response(content=graph_image, media_type='image/png')
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

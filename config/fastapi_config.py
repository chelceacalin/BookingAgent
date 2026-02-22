from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.chatbot import chatbot
from api.memory import memory
from api.server import server
from .logging_config import logger

app = FastAPI()
app.include_router(chatbot)
app.include_router(memory, prefix="/memory")
app.include_router(server, prefix="/server")


@app.middleware("http")
async def before_request(request: Request, call_next):
    if request.url.path == "/chat" and request.headers.get("content-type") == "application/json":
        body = await request.json()
        query = body.get("query", None)
        if query:
            logger.info("Got query: " + str(query))
    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def handle_error(request: Request, e: Exception):
    logger.error(e)
    return JSONResponse(status_code=500, content={"error": str(e)})

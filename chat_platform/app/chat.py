import logging
from app.ws_manager import ConnectionManager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


conn_manager = ConnectionManager()

logger = logging.getLogger("uvicorn")

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/chatroom/{username}")
async def chatroom_page_endpoint(request: Request, username: str):
    
    return templates.TemplateResponse(
        request=request,
        name="chatroom.html",
        context={"username": username}
    )
    




@router.websocket("/chatroom/{username}")
async def chatroom_endpoint(
    websocket: WebSocket, username: str
):
    await conn_manager.connect(websocket)
    await conn_manager.broadcast(
        f"{username} joined the chat",
        exclude=websocket,
    )
    logger.info(f"{username} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await conn_manager.broadcast(
                {"sender": username, "message": data},
                exclude=websocket,
            )
            await conn_manager.send_personal_message(
                {"sender": "You", "message": data},
                websocket,
            )
    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        await conn_manager.broadcast(
            {
                "sender": "system",
                "message": f"Client #{username} "
                "left the chat",
            }
        )
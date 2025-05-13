import logging
import asyncio

from fastapi import FastAPI, status
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.exceptions import WebSocketException
from app.chat import router as chat_router


logger = logging.getLogger("uvicorn")

app = FastAPI()
app.include_router(chat_router)






@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    await websocket.send_text("Welcome to the chat room!")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Message received: {data}")
            await websocket.send_text(f"You said: {data}")
            if data == "disconnect":
                logger.warning("Disconnecting...")
                await asyncio.sleep(4)
                return await websocket.close(code=status.WS_1000_NORMAL_CLOSURE, reason="Disconnecting...",)
            if "bad message" in data:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Inappropriate message"
                )
    except WebSocketDisconnect:
        logger.warning("Connection closed by the client ")
    
    await websocket.close()
    



@app.websocket("/secured-ws")
async def secured_websocket(
    websocket: WebSocket,
    username: str
):
    await websocket.accept()
    await websocket.send_text(f"Welcome {username}!")
    async for data in websocket.iter_text():
        await websocket.send_text(
            f"You wrote: {data}"
        )






from fastapi import APIRouter, WebSocket
from main import WS_MESSAGE_BUS
from src.utils.message_bus import WebsocketAsyncBusMessageHandler


router = APIRouter(prefix="/ws")


@router.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    handler = WebsocketAsyncBusMessageHandler(websocket=websocket)
    await websocket.send_json({"accepted": "true"})
    await WS_MESSAGE_BUS.subscribe(handler)
    while True:
        data = await websocket.receive_text()
        if data:
            await websocket.send_json({"msg": "Readonly websocket connection"})
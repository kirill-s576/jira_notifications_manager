from fastapi import APIRouter, Request, WebSocket
from settings import WS_MESSAGE_BUS
from src.utils.message_bus import BusMessage, AbstractAsyncBusMessageHandler


router = APIRouter(prefix="/ws")


@router.get("/test_message", tags=["WS"])
async def test_message(request: Request):
    await WS_MESSAGE_BUS.add_message(BusMessage(payload={"url": "test_message"}))
    return ""


@router.get("/test_message2", tags=["WS"])
async def test_message2(request: Request):
    await WS_MESSAGE_BUS.add_message(BusMessage(payload={"url": "test_message2"}))
    return ""


class WsHandler(AbstractAsyncBusMessageHandler):

    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        super().__init__()

    async def handle_message(self, message: BusMessage):
        await self.websocket.send_json(message.payload)


@router.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    handler = WsHandler(websocket=websocket)
    await websocket.send_json({"accepted": "true"})
    await WS_MESSAGE_BUS.subscribe(handler)
    while True:
        data = await websocket.receive_text()
        print(data)
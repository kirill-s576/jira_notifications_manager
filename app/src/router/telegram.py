from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from settings import WS_MESSAGE_BUS, APP_CONFIG
from src.utils.message_bus import BusMessage
import aiogram
import json

router = APIRouter(prefix="/telegram")

BOT = aiogram.Bot(token=APP_CONFIG.TELEGRAM_BOT_TOKEN)


@router.post(f"/webhook/{APP_CONFIG.TELEGRAM_BOT_TOKEN}", tags=["Telegram"], include_in_schema=False)
async def webhook_handle(request: Request):
    """

    """
    message = {
        "telegram_webhook": request.json()
    }
    await WS_MESSAGE_BUS.add_message(message=BusMessage(payload=message))
    return PlainTextResponse("true", status_code=200)


@router.post(f"/webhook/set", tags=["Telegram"])
async def webhook_set(request: Request):
    """

    """
    url = f"https://{APP_CONFIG.SERVER_HOST}/telegram/webhook/{APP_CONFIG.TELEGRAM_BOT_TOKEN}"
    response = await BOT.set_webhook(url=url)
    return JSONResponse({"result": response}, status_code=200)


@router.post(f"/webhook/remove", tags=["Telegram"])
async def webhook_remove(request: Request):
    """

    """
    response = await BOT.delete_webhook(drop_pending_updates=True)
    return JSONResponse({"result": response}, status_code=200)


@router.get(f"/webhook/info", tags=["Telegram"])
async def webhook_info(request: Request):
    """

    """
    response = await BOT.get_webhook_info()
    return JSONResponse(json.loads(response.as_json()), status_code=200)
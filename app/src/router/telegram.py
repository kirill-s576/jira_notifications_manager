from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from settings import WS_MESSAGE_BUS, APP_CONFIG
from src.utils.message_bus import BusMessage
from src.services.telegram.bot import JiraBot
import json


router = APIRouter(prefix="/telegram")
BOT = JiraBot(APP_CONFIG.TELEGRAM_BOT_TOKEN)


@router.post("/webhook/handle/{telegram_bot_token}", tags=["Telegram"])
async def webhook_handle(request: Request, telegram_bot_token: str):
    """

    """
    if telegram_bot_token != APP_CONFIG.TELEGRAM_BOT_TOKEN:
        return PlainTextResponse("Bot with this token not found", status_code=404)
    request_data = await request.json()
    await WS_MESSAGE_BUS.add_message(message=BusMessage(payload=request_data))
    try:
        await BOT.process_update(request_data)
        return PlainTextResponse("true", status_code=200)
    except Exception as e:
        return PlainTextResponse(str(e), status_code=500)


@router.post(f"/webhook/set", tags=["Telegram"])
async def webhook_set():
    """

    """
    url = f"https://{APP_CONFIG.SERVER_HOST}/telegram/webhook/handle/{APP_CONFIG.TELEGRAM_BOT_TOKEN}"
    response = await BOT.bot.set_webhook(url=url)
    return JSONResponse({"result": response}, status_code=200)


@router.post(f"/webhook/remove", tags=["Telegram"])
async def webhook_remove():
    """

    """
    response = await BOT.bot.delete_webhook(drop_pending_updates=True)
    return JSONResponse({"result": response}, status_code=200)


@router.get(f"/webhook/info", tags=["Telegram"])
async def webhook_info():
    """

    """
    response = await BOT.bot.get_webhook_info()
    response_dict = json.loads(response.as_json())
    response_dict["url"] = response_dict["url"].replace(
        f"{APP_CONFIG.TELEGRAM_BOT_TOKEN}", "<BOT_TOKEN>"
    )
    return JSONResponse(response_dict, status_code=200)

from fastapi import APIRouter, Request, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from settings import APP_CONFIG
from src.services.telegram.bot_service import JiraBotAsyncService
import json


router = APIRouter(prefix="/telegram")
BOT = JiraBotAsyncService(APP_CONFIG.TELEGRAM_BOT_TOKEN)


@router.post("/webhook/handle/{telegram_bot_token}", tags=["Telegram"])
async def webhook_handle(
        request: Request,
        telegram_bot_token: str
):
    """

    """
    bot = JiraBotAsyncService(token=APP_CONFIG.TELEGRAM_BOT_TOKEN)
    request_data = await request.json()
    await bot.process_update(request_data)
    return PlainTextResponse("true", status_code=200)


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


@router.post(f"/emulate_tg_webhook", tags=["General"])
async def test_endpoint(
    telegram_webhook: dict = Body()
):
    """

    """
    service = JiraBotAsyncService(APP_CONFIG.TELEGRAM_BOT_TOKEN)
    await service.process_update(telegram_webhook)
    r = {}
    return JSONResponse(r, status_code=200)

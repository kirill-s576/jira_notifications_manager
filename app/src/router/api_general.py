from fastapi import APIRouter, Request, HTTPException, Body
from fastapi.responses import JSONResponse
from src.services.telegram.bot_service import JiraBotAsyncService
from settings import APP_CONFIG


router = APIRouter(prefix="/general")


async def verify_query_params_token(
        token: str
):
    if token != "12345":
        raise HTTPException(status_code=403, detail="Token query params invalid")


@router.post(f"/test", tags=["General"])
async def test_endpoint(
        request: Request,
        telegram_webhook: dict = Body()
):
    """

    """
    import json
    service = JiraBotAsyncService(APP_CONFIG.TELEGRAM_BOT_TOKEN)
    await service.process_update(telegram_webhook)
    r = {}
    return JSONResponse(r, status_code=200)

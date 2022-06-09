from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from typing import Optional

from settings import APP_CONFIG
from src.services.telegram.web_app_service import WebAppAsyncService, WebAppUser
from logging import getLogger
from settings import LogConfig


logger = getLogger(LogConfig().LOGGER_NAME)


router = APIRouter(prefix="/web_app")


@router.get(f"/verify_init_data", tags=["TelegramWebApp"], response_model=WebAppUser)
async def verify_init_data(init_data: str):
    logger.debug(f"verify_init_data:INIT_DATA: {init_data}")
    service = WebAppAsyncService(
        init_data=init_data,
        bot_token=APP_CONFIG.TELEGRAM_BOT_TOKEN
    )
    user = service.verified_init_data.safe_init_data_object.user
    return user


class JiraAccountResponseModel(BaseModel):
    id: str
    resource_id: str
    resource_name: str
    resource_url: Optional[str]
    avatar_url: Optional[str]
    scopes: List[str] = []


@router.get(f"/jira_accounts", tags=["TelegramWebApp"], response_model=List[JiraAccountResponseModel])
async def get_jira_accounts(
    init_data: str = Header()
):
    """

    """
    logger.debug(f"get_jira_account:INIT_DATA: {init_data}")
    service = WebAppAsyncService(
        init_data=init_data,
        bot_token=APP_CONFIG.TELEGRAM_BOT_TOKEN
    )
    accounts = await service.get_jira_accounts()
    response = [
        JiraAccountResponseModel(id=str(account.id), **account.dict(exclude={"id"})) for account in accounts
    ]
    return response


@router.post(f"/jira_accounts", tags=["TelegramWebApp"])
async def add_new_jira_account(
    init_data: str = Header()
):
    logger.debug(f"add_new_jira_account:INIT_DATA: {init_data}")
    web_app_service = WebAppAsyncService(
        init_data=init_data,
        bot_token=APP_CONFIG.TELEGRAM_BOT_TOKEN
    )
    await web_app_service.add_jira_account()
    return JSONResponse({"msg": "Ok"}, status_code=200)

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from settings import WS_MESSAGE_BUS, APP_CONFIG
from src.utils.message_bus import BusMessage
from src.utils.jira_async_api import JiraOAuthAsyncApi


router = APIRouter(prefix="/auth")


@router.get("/login", tags=["Auth"])
async def login(request: Request):
    """

    """
    api = JiraOAuthAsyncApi(
        client_id=APP_CONFIG.JIRA_APP_CLIENT_ID,
        client_secret=APP_CONFIG.JIRA_APP_SECRET,
        redirect_uri=f"https://{APP_CONFIG.SERVER_HOST}/auth/confirm_oauth",
        scope=APP_CONFIG.JIRA_AUTH_SCOPE_LIST
    )
    return RedirectResponse(
        api.get_redirect_uri(),
        status_code=301
    )


@router.get("/confirm_oauth", tags=["Auth"])
async def confirm_oauth(request: Request, code: str, state: str):
    """

    """
    message = {
        "oauth_code": code,
        "oauth_state": state
    }
    await WS_MESSAGE_BUS.add_message(message=BusMessage(payload=message))
    return RedirectResponse("/telegram/jira_accs", status_code=301)
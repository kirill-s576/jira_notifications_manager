from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from settings import WS_MESSAGE_BUS, APP_CONFIG
from src.utils.message_bus import BusMessage
from src.utils.jira_async_api import JiraOAuthAsyncApi
import urllib.parse


router = APIRouter(prefix="/auth")
jira_auth_api = JiraOAuthAsyncApi(
    client_id=APP_CONFIG.JIRA_APP_CLIENT_ID,
    client_secret=APP_CONFIG.JIRA_APP_SECRET,
    redirect_uri=urllib.parse.quote(f"https://{APP_CONFIG.SERVER_HOST}/auth/confirm_oauth"),
    scope=APP_CONFIG.JIRA_AUTH_SCOPE_LIST
)


@router.get("/login", tags=["Auth"])
async def login(request: Request):
    """

    """

    uri = jira_auth_api.get_auth_uri(user_state="12345678")
    return RedirectResponse(
        uri,
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
            "Expires": "Sat, 26 Jul 1997 05:00:00 GMT"
        },
        status_code=307
    )


@router.get("/confirm_oauth", tags=["Auth"])
async def confirm_oauth(request: Request, code: str, state: str):
    """

    """
    message = {
        "oauth_code": code,
        "oauth_state": state
    }
    auth_data = await jira_auth_api.exchange_code_to_jwt(code)
    await WS_MESSAGE_BUS.add_message(message=BusMessage(payload=message))
    await WS_MESSAGE_BUS.add_message(message=BusMessage(payload=auth_data))
    return RedirectResponse(
        "/telegram/jira_accs",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
            "Expires": "Sat, 26 Jul 1997 05:00:00 GMT"
        },
        status_code=307
    )
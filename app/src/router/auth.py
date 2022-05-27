from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from settings import WS_MESSAGE_BUS
from src.utils.message_bus import BusMessage


router = APIRouter(prefix="/auth")


@router.get("/login", tags=["Auth"])
async def login(request: Request):
    """

    """
    return RedirectResponse(
        "https://auth.atlassian.com"
        "/authorize"
        "?"
        "audience=api.atlassian.com"
        "&client_id=zAvXEQkzZDMMFvuhv7WHoJ5JcKGzEHlM"
        "&scope=read%3Ajira-user%20manage%3Ajira-webhook%20read%3Ajira-work"
        "&redirect_uri=https%3A%2F%2Fk.dserdiuk.com%2Fauth%2Fconfirm_oauth"
        "&state=1357908642"
        "&response_type=code"
        "&prompt=consent",
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
    return RedirectResponse("/", status_code=301)
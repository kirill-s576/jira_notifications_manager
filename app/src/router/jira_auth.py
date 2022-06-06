from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from settings import APP_CONFIG
from src.services.jira.auth_service import JiraAuthAsyncService


router = APIRouter(prefix="/jira_auth")


@router.get("/login", tags=["Auth"], response_class=RedirectResponse)
async def login(user_state: str):
    """
    Redirect to Jira login page for oAuth 2.0
    """
    service = JiraAuthAsyncService()
    redirect_uri = service.get_auth_uri(user_state=user_state)
    return RedirectResponse(
        redirect_uri,
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
            "Expires": "Sat, 26 Jul 1997 05:00:00 GMT"
        },
        status_code=307
    )


@router.get("/confirm_oauth", tags=["Auth"], response_class=RedirectResponse)
async def confirm_oauth(code: str, state: str):
    """
    Redirect URI for Jira oAuth 2.0.
    Redirect to Telegram application.
    """
    service = JiraAuthAsyncService()
    redirect_uri = await service.confirm_oauth(code, state)
    return RedirectResponse(
        redirect_uri,
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
            "Expires": "Sat, 26 Jul 1997 05:00:00 GMT"
        },
        status_code=307
    )

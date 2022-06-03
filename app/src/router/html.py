from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from settings import APP_CONFIG


router = APIRouter(prefix="")
templates = Jinja2Templates(directory="templates")


def get_websocket_url():
    websocket_url = ""
    if APP_CONFIG.SERVER_SSL:
        websocket_url += "wss://"
    else:
        websocket_url += "ws://"
    websocket_url += APP_CONFIG.SERVER_HOST
    if int(APP_CONFIG.SERVER_PORT) != 80:
        websocket_url += f"{APP_CONFIG.SERVER_PORT}"
    websocket_url += "/ws/websocket"
    return websocket_url


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request
    })


@router.get("/auth", response_class=HTMLResponse, include_in_schema=False)
async def auth(request: Request):
    return templates.TemplateResponse("auth.html", {
        "request": request
    })


@router.get("/admin_settings", response_class=HTMLResponse, include_in_schema=False)
async def auth(request: Request):
    return templates.TemplateResponse("admin_settings.html", {
        "request": request
    })


@router.get(f"/telegram/web_app_main_page", include_in_schema=False)
async def tg_web_app_main_page(request: Request):
    """

    """
    return templates.TemplateResponse("tg_web_app_main_page.html", {
        "request": request
    })


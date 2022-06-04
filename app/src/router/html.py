from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime


router = APIRouter(prefix="")
templates = Jinja2Templates(directory="templates")
templates.env.globals["now"] = datetime.datetime.utcnow


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


@router.get(f"/telegram/jira_accs", include_in_schema=False)
async def tg_web_app_main_page(request: Request):
    """

    """
    return templates.TemplateResponse("tg_web_app_jira_accs.html", {
        "request": request,
        "login_path": "/auth/login"
    })

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.router import example, websocket_logger
import settings


app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static, media and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Include routers.
app.include_router(example.router)
app.include_router(websocket_logger.router)


@app.get("/home", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    websocket_url = ""
    if settings.SERVER_SSL:
        websocket_url += "wss://"
    else:
        websocket_url += "ws://"
    websocket_url += settings.SERVER_HOST
    if int(settings.SERVER_PORT) != 80:
        websocket_url += f"{settings.SERVER_PORT}"
    websocket_url += "/ws/websocket"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "websocket_url": websocket_url
    })



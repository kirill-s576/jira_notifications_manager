from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import (
    websocket_logger,
    auth,
    html
)
from settings import Settings
from src.utils.message_bus import AsyncMessageBus


settings = Settings()
app = FastAPI()
WS_MESSAGE_BUS = AsyncMessageBus()


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers.
app.include_router(html.router)
app.include_router(auth.router)
app.include_router(websocket_logger.router)

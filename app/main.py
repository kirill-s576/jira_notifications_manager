from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import (
    websocket,
    jira_auth,
    html,
    api_telegram,
    api_web_app
)


app = FastAPI()


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
app.include_router(jira_auth.router)
app.include_router(websocket.router)
app.include_router(api_telegram.router)
app.include_router(api_web_app.router)

from email import header
from re import I
from tkinter.messagebox import NO
from fastapi import APIRouter, Request


router = APIRouter(prefix="/auth")


@router.get("/login", tags=["Auth"])
async def login(request: Request):
    return ""


@router.get("/confirm_oauth", tags=["Auth"])
async def confirm_oauth(request: Request):
    """
    """
    return ""
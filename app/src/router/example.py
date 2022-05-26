from email import header
from re import I
from fastapi import APIRouter, Request


router = APIRouter(prefix="/example")


@router.get("/", tags=["Example"], response_model=None, openapi_extra={
    
})
async def get_example(request: Request):
    return ""
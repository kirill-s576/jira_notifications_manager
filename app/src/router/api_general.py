from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import functools


router = APIRouter(prefix="/general")


def wrapper(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        print("Decorator")
        print(kwargs)
        request: Request = kwargs.get("request")
        token = request.query_params.get("token")
        if token != "12345":
            return JSONResponse({"message": "Incorrect token"}, status_code=403)
        return await func(*args, **kwargs)
    return wrapped


@router.get(f"/test", tags=["General"])
@wrapper
async def webhook_info(request: Request, token: str):
    """

    """
    response_dict = {}
    return JSONResponse(response_dict, status_code=200)

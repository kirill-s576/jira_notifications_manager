from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/general")


async def verify_query_params_token(
        token: str
):
    if token != "12345":
        raise HTTPException(status_code=403, detail="Token query params invalid")


@router.get(f"/test", tags=["General"])
async def test_endpoint(
        request: Request
):
    """

    """
    r = {}
    return JSONResponse(r, status_code=200)

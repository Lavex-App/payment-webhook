from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

pix_webhook_controller = APIRouter()


@pix_webhook_controller.post("/", status_code=status.HTTP_201_CREATED)
async def verify_notification() -> JSONResponse:
    return JSONResponse(content={"hello": "world"})


@pix_webhook_controller.post("/pix")
async def receive_notification() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"hello": "world"})

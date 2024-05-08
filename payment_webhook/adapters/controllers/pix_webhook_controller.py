from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from payment_webhook.adapters.controllers.__dependencies__ import PixStatusChangeReceiverControllerDependencies
from payment_webhook.business.ports import PaymentReceivedInputPort

pix_webhook_controller = APIRouter(prefix="/webhook")


@pix_webhook_controller.post("/", status_code=status.HTTP_201_CREATED)
async def verify_webhook() -> JSONResponse:
    return JSONResponse(content={"status": 200})


@pix_webhook_controller.post("/pix")
async def pix_status_change_receiver(
    dependencies: Annotated[PixStatusChangeReceiverControllerDependencies, Depends()],
    pix_status_change: list[dict[str, str]] = Body(None),
) -> JSONResponse:
    for pix in pix_status_change:
        if "txid" in pix and "devolucoes" not in pix:
            input_port = PaymentReceivedInputPort(txid=pix["txid"], payment_time=pix["horario"])
            await dependencies.payment_received_use_case(input_port)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"hello": "world"})

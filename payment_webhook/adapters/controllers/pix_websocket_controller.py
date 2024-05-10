import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from payment_webhook.business.ports import (
    CancelPaymentReceiptCheckInputPort,
    CheckPaymentOfClientInTheQueueInputPort,
    SaveClientInWaitingQueueInputPort,
)
from payment_webhook.models import ClientConnectionStatus

from .__dependencies__ import Waiting2ReceivePaymentControllerDependencies

pix_websocket_controller = APIRouter(prefix="/ws")


@pix_websocket_controller.websocket("/waiting2receive-payment")
async def waiting2receive_payment(
    websocket: WebSocket,
    dependencies: Annotated[Waiting2ReceivePaymentControllerDependencies, Depends()],
) -> None:
    await websocket.accept()
    save_clients_in_waiting_queue_input_port = SaveClientInWaitingQueueInputPort(uid=dependencies.uid)
    await dependencies.save_clients_in_waiting_queue_use_case(save_clients_in_waiting_queue_input_port)

    async def check_receipt_of_payment() -> None:
        payment_was_checked = False
        while not payment_was_checked:
            try:
                input_port = CheckPaymentOfClientInTheQueueInputPort(uid=dependencies.uid)
                output_port = await dependencies.check_payment_of_client_in_the_queue_use_case(input_port)
                payment_was_checked = output_port.status == ClientConnectionStatus.PAID
            except WebSocketDisconnect:
                break

    async def check_payment_cancellation() -> None:
        while True:
            try:
                message = await websocket.receive_json(mode="text")
                if "cancel_payment" in message:
                    input_port = CancelPaymentReceiptCheckInputPort(uid=dependencies.uid)
                    await dependencies.cancel_payment_receipt_check_use_case(input_port)
            except WebSocketDisconnect:
                break

    tasks = [
        asyncio.create_task(check_receipt_of_payment()),
        asyncio.create_task(check_payment_cancellation()),
    ]
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

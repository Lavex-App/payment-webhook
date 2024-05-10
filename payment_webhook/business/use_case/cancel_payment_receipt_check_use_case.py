from typing import NamedTuple

from ..ports import CancelPaymentReceiptCheckInputPort, CancelPaymentReceiptCheckOutputPort
from ..services import ClientQueueCancellerService
from .interfaces import UseCase


class CancelPaymentReceiptCheckServices(NamedTuple):
    client_queue_canceller_service: ClientQueueCancellerService


class CancelPaymentReceiptCheckUseCase(
    UseCase[CancelPaymentReceiptCheckInputPort, CancelPaymentReceiptCheckOutputPort]
):
    def __init__(self, services: CancelPaymentReceiptCheckServices) -> None:
        self.__client_queue_canceller_service = services.client_queue_canceller_service

    async def __call__(self, input_port: CancelPaymentReceiptCheckInputPort) -> CancelPaymentReceiptCheckOutputPort:
        await self.__client_queue_canceller_service.cancel_client_waiting_in_queue(input_port)
        return CancelPaymentReceiptCheckOutputPort(msg="ok")

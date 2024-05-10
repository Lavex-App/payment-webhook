from typing import NamedTuple

from ..ports import CheckPaymentOfClientInTheQueueInputPort, CheckPaymentOfClientInTheQueueOutputPort
from ..services import QueueAdministratorService
from .interfaces import UseCase


class CheckPaymentOfClientInTheQueueServices(NamedTuple):
    queue_administrator_service: QueueAdministratorService


class CheckPaymentOfClientInTheQueueUseCase(
    UseCase[CheckPaymentOfClientInTheQueueInputPort, CheckPaymentOfClientInTheQueueOutputPort]
):
    def __init__(self, services: CheckPaymentOfClientInTheQueueServices) -> None:
        self.__queue_administrator_service = services.queue_administrator_service

    async def __call__(
        self, input_port: CheckPaymentOfClientInTheQueueInputPort
    ) -> CheckPaymentOfClientInTheQueueOutputPort:
        connected_client = await self.__queue_administrator_service.find_client_in_queue(input_port)
        return CheckPaymentOfClientInTheQueueOutputPort(**connected_client.model_dump(), msg="ok")

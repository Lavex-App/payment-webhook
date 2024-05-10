from typing import NamedTuple

from ..ports import SaveClientInWaitingQueueInputPort, SaveClientInWaitingQueueOutputPort
from ..services import ClientQueueAdderService
from .interfaces import UseCase


class SaveClientInWaitingQueueServices(NamedTuple):
    client_queue_adder_service: ClientQueueAdderService


class SaveClientInWaitingQueueUseCase(UseCase[SaveClientInWaitingQueueInputPort, SaveClientInWaitingQueueOutputPort]):
    def __init__(self, services: SaveClientInWaitingQueueServices) -> None:
        self.__client_queue_adder_service = services.client_queue_adder_service

    async def __call__(self, input_port: SaveClientInWaitingQueueInputPort) -> SaveClientInWaitingQueueOutputPort:
        await self.__client_queue_adder_service.add2queueIfItIsNot(input_port)
        return SaveClientInWaitingQueueOutputPort(msg="ok")

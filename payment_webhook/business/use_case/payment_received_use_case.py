from typing import NamedTuple

from payment_webhook.models import ClientConnectionStatus, ConnectedClientModel

from ..ports import PaymentReceivedInputPort, PaymentReceivedOutputPort
from ..services import AccountService, EventService, QueueAdministratorService
from .interfaces import UseCase


class PaymentReceivedServices(NamedTuple):
    account_service: AccountService
    event_service: EventService
    queue_administrator_service: QueueAdministratorService


class PaymentReceivedUseCase(UseCase[PaymentReceivedInputPort, PaymentReceivedOutputPort]):
    def __init__(self, services: PaymentReceivedServices) -> None:
        self.__account_service = services.account_service
        self.__event_service = services.event_service
        self.__queue_administrator_service = services.queue_administrator_service

    async def __call__(self, input_port: PaymentReceivedInputPort) -> PaymentReceivedOutputPort:
        paying_user = await self.__account_service.retrieve_paying_user(input_port)
        await self.__event_service.trigger(paying_user)
        updated_connected_client = ConnectedClientModel(uid=paying_user.uid, status=ClientConnectionStatus.PAID)
        await self.__queue_administrator_service.change_client_status(updated_connected_client)
        return PaymentReceivedOutputPort(msg="ok")

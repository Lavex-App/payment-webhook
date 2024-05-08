from typing import NamedTuple

from ..ports import PaymentReceivedInputPort, PaymentReceivedOutputPort
from ..services import AccountService, EventService, NotificationService
from .interfaces import UseCase


class PaymentReceivedServices(NamedTuple):
    account_service: AccountService
    event_service: EventService
    notification_service: NotificationService


class PaymentReceivedUseCase(UseCase[PaymentReceivedInputPort, PaymentReceivedOutputPort]):
    def __init__(self, services: PaymentReceivedServices) -> None:
        self.__account_service = services.account_service
        self.__event_service = services.event_service
        self.__notification_service = services.notification_service

    async def __call__(self, input_port: PaymentReceivedInputPort) -> PaymentReceivedOutputPort:
        paying_user = await self.__account_service.retrieve_paying_user(input_port)
        await self.__event_service.trigger(paying_user)
        await self.__notification_service.trigger(paying_user)
        return PaymentReceivedOutputPort(msg="ok")

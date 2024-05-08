from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from payment_webhook.business.use_case import PaymentReceivedServices, PaymentReceivedUseCase

from .services import AccountService, EventService, NotificationService

T_account_service_co = TypeVar("T_account_service_co", bound=AccountService, covariant=True)
T_event_service_co = TypeVar("T_event_service_co", bound=EventService, covariant=True)
T_notification_service_co = TypeVar("T_notification_service_co", bound=NotificationService, covariant=True)


# noinspection PyTypeHints
class AdaptersFactoryInterface(
    Generic[
        T_account_service_co,
        T_event_service_co,
        T_notification_service_co,
    ],
    metaclass=ABCMeta,
):
    @abstractmethod
    def account_service(self) -> T_account_service_co: ...

    @abstractmethod
    def event_service(self) -> T_event_service_co: ...

    @abstractmethod
    def notification_service(self) -> T_notification_service_co: ...


class BusinessFactory:
    def __init__(self, adapters_factory: AdaptersFactoryInterface) -> None:
        self.__factory = adapters_factory

    def payment_received_use_case(self) -> PaymentReceivedUseCase:
        services = PaymentReceivedServices(
            account_service=self.__factory.account_service(),
            event_service=self.__factory.event_service(),
            notification_service=self.__factory.notification_service(),
        )
        return PaymentReceivedUseCase(services)

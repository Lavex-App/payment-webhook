from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from payment_webhook.business.use_case import (
    CancelPaymentReceiptCheckServices,
    CancelPaymentReceiptCheckUseCase,
    CheckPaymentOfClientInTheQueueServices,
    CheckPaymentOfClientInTheQueueUseCase,
    PaymentReceivedServices,
    PaymentReceivedUseCase,
    SaveClientInWaitingQueueServices,
    SaveClientInWaitingQueueUseCase,
)

from .services import AccountService, EventService, QueueService

T_account_service_co = TypeVar("T_account_service_co", bound=AccountService, covariant=True)
T_event_service_co = TypeVar("T_event_service_co", bound=EventService, covariant=True)
T_in_memory_storage_service_co = TypeVar("T_in_memory_storage_service_co", bound=QueueService, covariant=True)


# noinspection PyTypeHints
class AdaptersFactoryInterface(
    Generic[
        T_account_service_co,
        T_event_service_co,
        T_in_memory_storage_service_co,
    ],
    metaclass=ABCMeta,
):
    @abstractmethod
    def account_service(self) -> T_account_service_co: ...

    @abstractmethod
    def event_service(self) -> T_event_service_co: ...

    @abstractmethod
    def in_memory_storage_service(self) -> T_in_memory_storage_service_co: ...


class BusinessFactory:
    def __init__(self, adapters_factory: AdaptersFactoryInterface) -> None:
        self.__factory = adapters_factory

    def payment_received_use_case(self) -> PaymentReceivedUseCase:
        services = PaymentReceivedServices(
            account_service=self.__factory.account_service(),
            event_service=self.__factory.event_service(),
            queue_administrator_service=self.__factory.in_memory_storage_service(),
        )
        return PaymentReceivedUseCase(services)

    def save_client_in_waiting_queue_use_case(self) -> SaveClientInWaitingQueueUseCase:
        services = SaveClientInWaitingQueueServices(
            client_queue_adder_service=self.__factory.in_memory_storage_service(),
        )
        return SaveClientInWaitingQueueUseCase(services)

    def check_payment_of_client_in_the_queue_use_case(self) -> CheckPaymentOfClientInTheQueueUseCase:
        services = CheckPaymentOfClientInTheQueueServices(
            queue_administrator_service=self.__factory.in_memory_storage_service(),
        )
        return CheckPaymentOfClientInTheQueueUseCase(services)

    def cancel_payment_receipt_check_use_case(self) -> CancelPaymentReceiptCheckUseCase:
        services = CancelPaymentReceiptCheckServices(
            client_queue_canceller_service=self.__factory.in_memory_storage_service(),
        )
        return CancelPaymentReceiptCheckUseCase(services)

from abc import ABCMeta, abstractmethod

from payment_webhook.models import AuthenticatedUserModel, ConnectedClientModel, PayingUserModel

from .interfaces import Service
from .ports import PaymentReceivedInputPort


class EventService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def trigger(self, port: PayingUserModel) -> None: ...


class AccountService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def retrieve_paying_user(self, port: PaymentReceivedInputPort) -> PayingUserModel: ...


class ClientQueueAdderService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def add2queueIfItIsNot(self, port: AuthenticatedUserModel) -> None: ...


class QueueAdministratorService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def find_client_in_queue(self, port: AuthenticatedUserModel) -> ConnectedClientModel: ...

    @abstractmethod
    async def change_client_status(self, port: ConnectedClientModel) -> None: ...


class ClientQueueCancellerService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def cancel_client_waiting_in_queue(self, port: AuthenticatedUserModel) -> None: ...


class QueueService(
    ClientQueueAdderService,
    QueueAdministratorService,
    ClientQueueCancellerService,
    metaclass=ABCMeta,
): ...

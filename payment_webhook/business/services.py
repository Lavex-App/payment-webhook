from abc import ABCMeta, abstractmethod

from payment_webhook.models import PayingUser

from .interfaces import Service
from .ports import PaymentReceivedInputPort


class EventService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def trigger(self, port: PayingUser) -> None: ...


class NotificationService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def trigger(self, port: PayingUser) -> None: ...


class AccountService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def retrieve_paying_user(self, port: PaymentReceivedInputPort) -> PayingUser: ...

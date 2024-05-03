from abc import ABCMeta, abstractmethod

from payment_webhook.models import AuthenticatedUserModel

from .interfaces import Service


class ExampleService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def example(self, port: AuthenticatedUserModel) -> None: ...

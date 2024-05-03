from abc import ABCMeta, abstractmethod

from payment_webhook.models.user_model import AuthenticatedUserModel


class ExampleProvider(metaclass=ABCMeta):
    @abstractmethod
    async def example(self, user_model: AuthenticatedUserModel) -> None: ...

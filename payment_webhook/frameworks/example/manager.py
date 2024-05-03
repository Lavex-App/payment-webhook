from payment_webhook.adapters.interface_adapters.interfaces.example_provider import ExampleProvider
from payment_webhook.models.user_model import AuthenticatedUserModel


class ExampleManager(ExampleProvider):
    async def example(self, user_model: AuthenticatedUserModel) -> None:
        ...

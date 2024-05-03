from typing import NamedTuple

from payment_webhook.models import AuthenticatedUserModel

from .interfaces import ExampleProvider

class ExampleAdapterConfig(NamedTuple): ...


class ExampleProviders(NamedTuple):
    example_provider: ExampleProvider


class ExampleAdapter:
    def __init__(self, providers: ExampleProviders, config: ExampleAdapterConfig):
        self._providers = providers
        self._config = config

    async def example(self, user_model: AuthenticatedUserModel) -> None:
        await self._providers.example_provider(user_model)

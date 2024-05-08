from typing import NamedTuple

from payment_webhook.business.services import NotificationService
from payment_webhook.models import PayingUser

from .interfaces import InterfaceAdapter


class NotificationProviders(NamedTuple): ...


class NotificationAdapter(InterfaceAdapter, NotificationService):
    def __init__(self, providers: NotificationProviders):
        self._providers = providers

    async def trigger(self, port: PayingUser) -> None: ...

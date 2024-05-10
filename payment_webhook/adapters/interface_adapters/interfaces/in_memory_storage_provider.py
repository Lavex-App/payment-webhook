from abc import ABCMeta, abstractmethod

from payment_webhook.models import AuthenticatedUserModel


class ClientRegister(AuthenticatedUserModel):
    value: str


class StoringClientsInMemoryProvider(metaclass=ABCMeta):
    @abstractmethod
    async def find(self, client_uid: AuthenticatedUserModel) -> ClientRegister | None: ...

    @abstractmethod
    async def add(self, client: ClientRegister) -> None: ...

    @abstractmethod
    async def replace(self, updated_client: ClientRegister) -> None: ...

    @abstractmethod
    async def remove(self, client_uid: AuthenticatedUserModel) -> None: ...

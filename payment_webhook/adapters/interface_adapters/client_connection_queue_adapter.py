from typing import NamedTuple

from payment_webhook.business.services import QueueService
from payment_webhook.business.use_case import ClientIsNotInTheQueue
from payment_webhook.models import AuthenticatedUserModel, ClientConnectionStatus, ConnectedClientModel

from .interfaces import ClientRegister, InterfaceAdapter, StoringClientsInMemoryProvider


class ClientConnectionQueueProviders(NamedTuple):
    storing_clients_in_memory_provider: StoringClientsInMemoryProvider


class ClientConnectionQueueAdapter(InterfaceAdapter, QueueService):
    def __init__(self, providers: ClientConnectionQueueProviders) -> None:
        self.__storing_clients_in_memory_provider = providers.storing_clients_in_memory_provider

    async def add2queueIfItIsNot(self, port: AuthenticatedUserModel) -> None:
        client_register = ClientRegister(uid=port.uid, value=ClientConnectionStatus.WAITING_FOR_PAYMENT_CONFIRMATION)
        await self.__storing_clients_in_memory_provider.add(client_register)
        return None

    async def find_client_in_queue(self, port: AuthenticatedUserModel) -> ConnectedClientModel:
        client_register: ClientRegister | None = await self.__storing_clients_in_memory_provider.find(port)
        if client_register is not None:
            status = ClientConnectionStatus.from_value(client_register.value)
            return ConnectedClientModel(uid=client_register.uid, status=status)
        raise ClientIsNotInTheQueue()

    async def change_client_status(self, port: ConnectedClientModel) -> None:
        client_register = ClientRegister(uid=port.uid, value=port.status)
        await self.__storing_clients_in_memory_provider.replace(client_register)
        return None

    async def cancel_client_waiting_in_queue(self, port: AuthenticatedUserModel) -> None:
        await self.__storing_clients_in_memory_provider.remove(port)
        return None

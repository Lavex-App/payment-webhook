from typing import TypedDict

import aioredis

from payment_webhook.adapters.interface_adapters.interfaces import ClientRegister, StoringClientsInMemoryProvider
from payment_webhook.models import AuthenticatedUserModel


class RedisStorageFrameworkConfig(TypedDict):
    redis_host: str
    redis_port: int


class RedisStorageManager(StoringClientsInMemoryProvider):
    def __init__(self, config: RedisStorageFrameworkConfig) -> None:
        self.__app = aioredis.StrictRedis(host=config["redis_host"], port=config["redis_port"])

    async def find(self, client_uid: AuthenticatedUserModel) -> ClientRegister | None:
        value = await self.__app.get(client_uid.uid)
        if value is not None:
            return ClientRegister(uid=client_uid.uid, value=value)
        return None

    async def add(self, client: ClientRegister) -> None:
        set_only_if_does_not_exist = True
        await self.__app.set(client.uid, client.value, nx=set_only_if_does_not_exist)
        return None

    async def replace(self, updated_client: ClientRegister) -> None:
        client_register = await self.find(updated_client)
        if client_register is not None:
            await self.__app.set(updated_client.uid, updated_client.value)
        return None

    async def remove(self, client_uid: AuthenticatedUserModel) -> None:
        await self.__app.delete(client_uid.uid)
        return None

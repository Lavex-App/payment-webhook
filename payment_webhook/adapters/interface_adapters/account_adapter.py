from typing import Any, NamedTuple

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from payment_webhook.business.ports import PaymentReceivedInputPort
from payment_webhook.business.services import AccountService
from payment_webhook.models import PayingUser

from .exceptions import UserNotFound
from .interfaces import DatabaseName, DocumentDatabaseProvider, InterfaceAdapter

ProviderType = DocumentDatabaseProvider[AsyncIOMotorClient, AsyncIOMotorDatabase]


class AccountProviders(NamedTuple):
    document_database_provider: ProviderType


class AccountAdapter(InterfaceAdapter, AccountService):
    def __init__(self, providers: AccountProviders) -> None:
        database_provider = providers.document_database_provider
        database_provider.database = DatabaseName.PAYMENT  # type: ignore
        self.__payment_collection = database_provider.database["payment"]

    async def retrieve_paying_user(self, port: PaymentReceivedInputPort) -> PayingUser:
        payment: dict[str, Any] | None = await self.__payment_collection.find_one({"txid": port.txid})
        if payment:
            return PayingUser(**port.model_dump(), uid=payment["user_id"])
        raise UserNotFound()

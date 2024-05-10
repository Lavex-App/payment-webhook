import uuid
from datetime import datetime
from typing import NamedTuple

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from payment_webhook.business.services import EventService
from payment_webhook.models import PayingUserModel

from .interfaces import (
    DatabaseName,
    DocumentDatabaseProvider,
    Event,
    EventType,
    InterfaceAdapter,
    PublisherProvider,
    Topic,
)

ProviderType = DocumentDatabaseProvider[AsyncIOMotorClient, AsyncIOMotorDatabase]


class EventPublisherProviders(NamedTuple):
    publisher_provider: PublisherProvider
    document_database_provider: ProviderType


class EventPublisherAdapter(InterfaceAdapter, EventService):
    def __init__(self, providers: EventPublisherProviders):
        database_provider = providers.document_database_provider
        database_provider.database = DatabaseName.EVENT_ENGINE  # type: ignore
        self.__event_collection = database_provider.database["events"]
        self.__publisher_provider = providers.publisher_provider

    async def trigger(self, port: PayingUserModel) -> None:
        event = Event(
            transaction_id=str(uuid.uuid4()),
            event_id=str(uuid.uuid4()),
            event_type=EventType.PAYMENT_RECEIVED.value,
            event_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            payload=port.model_dump(),
        )
        self.__publisher_provider.publish(Topic.PAYMENT_RECEIVED, event)
        await self.__event_collection.insert_one(event.model_dump())

from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from fastapi import FastAPI

from payment_webhook.business.__factory__ import AdaptersFactoryInterface

from .controllers.__binding__ import Binding
from .interface_adapters import (
    AccountAdapter,
    AccountProviders,
    EventPublisherAdapter,
    EventPublisherProviders,
    NotificationAdapter,
    NotificationProviders,
)
from .interface_adapters.interfaces import AuthenticationProvider, DocumentDatabaseProvider, PublisherProvider

T_database_co = TypeVar("T_database_co", bound=DocumentDatabaseProvider, covariant=True)
T_authentication_co = TypeVar("T_authentication_co", bound=AuthenticationProvider, covariant=True)
T_publisher_co = TypeVar("T_publisher_co", bound=PublisherProvider, covariant=True)


class FrameworksFactoryInterface(Generic[T_database_co, T_authentication_co, T_publisher_co], metaclass=ABCMeta):
    @abstractmethod
    def database_provider(self) -> T_database_co: ...

    @abstractmethod
    def authentication_provider(self) -> T_authentication_co: ...

    @abstractmethod
    def publisher_provider(self) -> T_publisher_co: ...


class AdaptersFactory(AdaptersFactoryInterface[AccountAdapter, EventPublisherAdapter, NotificationAdapter]):
    def __init__(self, frameworks_factory: FrameworksFactoryInterface) -> None:
        self.__factory = frameworks_factory

    def account_service(self) -> AccountAdapter:
        providers = AccountProviders(document_database_provider=self.__factory.database_provider())
        return AccountAdapter(providers=providers)

    def event_service(self) -> EventPublisherAdapter:
        providers = EventPublisherProviders(
            publisher_provider=self.__factory.publisher_provider(),
            document_database_provider=self.__factory.database_provider(),
        )
        return EventPublisherAdapter(providers=providers)

    def notification_service(self) -> NotificationAdapter:
        providers = NotificationProviders()
        return NotificationAdapter(providers=providers)

    @staticmethod
    def register_routes(app: FastAPI) -> None:
        Binding().register_all(app)

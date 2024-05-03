from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from fastapi import FastAPI

from payment_webhook.business.__factory__ import AdaptersFactoryInterface

from .controllers.__binding__ import Binding
from .interface_adapters import ExampleAdapter, ExampleAdapterConfig, ExampleProviders
from .interface_adapters.interfaces import AuthenticationProvider, DocumentDatabaseProvider, ExampleProvider

T_database_co = TypeVar("T_database_co", bound=DocumentDatabaseProvider, covariant=True)
T_authentication_co = TypeVar("T_authentication_co", bound=AuthenticationProvider, covariant=True)
T_example_co = TypeVar("T_example_co", bound=ExampleProvider, covariant=True)


class FrameworksFactoryInterface(Generic[T_database_co, T_authentication_co], metaclass=ABCMeta):
    @abstractmethod
    def database_provider(self) -> T_database_co: ...

    @abstractmethod
    def authentication_provider(self) -> T_authentication_co: ...

    @abstractmethod
    def example_provider(self) -> T_example_co: ...


class AdaptersConfig(ExampleAdapterConfig): ...


class AdaptersFactory(AdaptersFactoryInterface[ExampleAdapter]):
    def __init__(self, frameworks_factory: FrameworksFactoryInterface, config: ExampleAdapterConfig) -> None:
        self.__factory = frameworks_factory
        self.__config = config

    def example_service(self) -> ExampleAdapter:
        providers = ExampleProviders(example_provider=self.__factory.example_provider())
        return ExampleAdapter(providers=providers, config=self.__config)

    @staticmethod
    def register_routes(app: FastAPI) -> None:
        Binding().register_all(app)

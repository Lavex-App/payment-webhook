from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from payment_webhook.business.use_case import ExampleServices, ExampleUseCase

from .services import ExampleService

T_example_service_co = TypeVar("T_example_service_co", bound=ExampleService, covariant=True)


# noinspection PyTypeHints
class AdaptersFactoryInterface(Generic[T_example_service_co], metaclass=ABCMeta):
    @abstractmethod
    def example_service(self) -> T_example_service_co: ...


class BusinessFactory:
    def __init__(self, adapters_factory: AdaptersFactoryInterface) -> None:
        self.__factory = adapters_factory

    def example_use_case(self) -> ExampleUseCase:
        services = ExampleServices(example_service=self.__factory.example_service())
        return ExampleUseCase(services)

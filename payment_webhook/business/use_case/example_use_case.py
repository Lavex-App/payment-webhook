from typing import NamedTuple

from ..ports import ExampleInputPort, ExampleOutputPort
from ..services import ExampleService
from .interfaces import UseCase


class ExampleServices(NamedTuple):
    example_service: ExampleService


class ExampleUseCase(UseCase[ExampleInputPort, ExampleOutputPort]):
    def __init__(self, services: ExampleServices) -> None:
        self.__example_service = services.example_service

    async def __call__(self, input_port: ExampleInputPort) -> ExampleOutputPort:
        await self.__example_service.example(input_port)
        return ExampleOutputPort(msg="ok")

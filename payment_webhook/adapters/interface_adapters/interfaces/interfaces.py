from abc import ABCMeta, abstractmethod

from .authentication_provider import AuthenticationProvider
from .document_database_provider import DocumentDatabaseProvider
from .example_provider import ExampleProvider


class InterfaceAdapter(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *providers: DocumentDatabaseProvider | AuthenticationProvider | ExampleProvider) -> None: ...

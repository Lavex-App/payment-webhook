from abc import ABCMeta, abstractmethod

from .authentication_provider import AuthenticationProvider
from .document_database_provider import DocumentDatabaseProvider
from .event_publisher_provider import PublisherProvider


class InterfaceAdapter(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *providers: DocumentDatabaseProvider | AuthenticationProvider | PublisherProvider) -> None: ...

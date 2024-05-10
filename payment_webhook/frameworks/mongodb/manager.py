import logging
from typing import TypedDict

import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from payment_webhook.adapters.interface_adapters.interfaces import DatabaseName, DocumentDatabaseProvider


class MotorFrameworkConfig(TypedDict):
    database_uri: str
    service_name: str
    sandbox: bool


class MotorManager(DocumentDatabaseProvider[AsyncIOMotorClient, AsyncIOMotorDatabase]):
    _database_name: str

    def __init__(self, config: MotorFrameworkConfig) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self.__service_name = config["service_name"]
        self.__database_uri = config["database_uri"]
        self.__sandbox = config["sandbox"]
        self.__app: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        self.close()
        try:
            self.__app = self.__get_app()
            await self.__app.admin.command("ping")
        except ConnectionFailure:  # pragma: no cover
            self._logger.info("Server [%s] not available!", self.__database_uri)
        else:
            self._logger.info("Connected to MongoDB")

    def close(self) -> None:
        if self.__app is None:
            return
        self.__app.close()
        self._logger.info("Closed MongoDB connection.")

    @property
    def client(self) -> AsyncIOMotorClient:
        if self.__app is None:
            raise ValueError("There is no MongoDB client.")
        return self.__app

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self.client[self._database_name]

    @database.setter
    def database(self, database_name: DatabaseName) -> None:
        self._database_name = database_name.value

    def __get_app(self) -> AsyncIOMotorClient:
        if self.__sandbox:
            return AsyncIOMotorClient(self.__database_uri, appname=self.__service_name)
        ca = certifi.where()
        return AsyncIOMotorClient(self.__database_uri, appname=self.__service_name, tls=True, tlsCAFile=ca)

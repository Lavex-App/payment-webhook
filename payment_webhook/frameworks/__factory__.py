from functools import lru_cache

from payment_webhook.adapters.__factory__ import FrameworksFactoryInterface

from .firebase import FirebaseFrameworkConfig, FirebaseManager
from .mongodb import MotorFrameworkConfig, MotorManager
from .pubsub import PubSubPublisherFrameworkConfig, PubSubPublisherManager


class FrameworksConfig:
    def __init__(
        self,
        firebase_framework_config: FirebaseFrameworkConfig,
        motor_framework_config: MotorFrameworkConfig,
        pubsub_publisher_framework_config: PubSubPublisherFrameworkConfig,
    ) -> None:
        self.firebase_framework_config = firebase_framework_config
        self.motor_framework_config = motor_framework_config
        self.pubsub_publisher_framework_config = pubsub_publisher_framework_config


class FrameworksFactory(FrameworksFactoryInterface[MotorManager, FirebaseManager, PubSubPublisherManager]):
    def __init__(self, config: FrameworksConfig) -> None:
        self.__config = config
        self.__motor_manager = MotorManager(config.motor_framework_config)

    async def connect(self) -> None:
        await self.__motor_manager.connect()

    async def close(self) -> None:
        self.__motor_manager.close()

    def database_provider(self) -> MotorManager:
        return self.__motor_manager

    def authentication_provider(self) -> FirebaseManager:
        return self.__firebase_manager

    def publisher_provider(self) -> PubSubPublisherManager:
        return PubSubPublisherManager(self.__config.pubsub_publisher_framework_config)

    def user_provider(self) -> FirebaseManager:
        return self.__firebase_manager

    @property
    @lru_cache
    def __firebase_manager(self) -> FirebaseManager:
        return FirebaseManager(self.__config.firebase_framework_config)

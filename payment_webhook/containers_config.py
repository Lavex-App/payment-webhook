from abc import ABCMeta
from functools import lru_cache

from environs import Env

from payment_webhook.adapters.__factory__ import AdaptersFactory
from payment_webhook.adapters.controllers.__dependencies__ import bind_controller_dependencies
from payment_webhook.business.__factory__ import BusinessFactory
from payment_webhook.frameworks.__factory__ import FrameworksConfig, FrameworksFactory
from payment_webhook.frameworks.firebase import FirebaseFrameworkConfig
from payment_webhook.frameworks.mongodb import MotorFrameworkConfig
from payment_webhook.frameworks.pubsub import PubSubPublisherFrameworkConfig
from payment_webhook.frameworks.redis import RedisStorageFrameworkConfig


class Config(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._env = Env(eager=True)
        self._env.read_env()

    @property
    @lru_cache
    def is_local(self) -> bool:
        return self._get_project_env == "local"

    @property
    @lru_cache
    def is_staging(self) -> bool:
        return self._get_project_env in ["dev", "staging"]

    @property
    @lru_cache
    def is_production(self) -> bool:
        return self._get_project_env == "main"

    @property
    @lru_cache
    def _get_project_env(self) -> str:
        return self._env.str("ENV", "main")


class ProjectConfig(Config):
    @property
    @lru_cache
    def frameworks_config(self) -> FrameworksConfig:
        return FrameworksConfig(
            motor_framework_config=self.__motor_framework_config,
            firebase_framework_config=self.__firebase_framework_config,
            pubsub_publisher_framework_config=self.__pubsub_publisher_framework_config,
            redis_storage_framework_config=self.__redis_storage_framework_config,
        )

    @property
    @lru_cache
    def __motor_framework_config(self) -> MotorFrameworkConfig:
        return MotorFrameworkConfig(
            database_uri=self._env.str("DB_URI"),
            service_name=self._env.str("SERVICE_NAME"),
            sandbox=self.is_local or self.is_staging,
        )

    @property
    @lru_cache
    def __firebase_framework_config(self) -> FirebaseFrameworkConfig:
        return FirebaseFrameworkConfig(
            credentials=self._env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
            auth_app_options={"projectId": self._env.str("PROJECT_ID")},
        )

    @property
    @lru_cache
    def __pubsub_publisher_framework_config(self) -> PubSubPublisherFrameworkConfig:
        return PubSubPublisherFrameworkConfig(
            credentials=self._env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
            project_id=self._env.str("PROJECT_ID"),
        )

    @property
    @lru_cache
    def __redis_storage_framework_config(self) -> RedisStorageFrameworkConfig:
        return RedisStorageFrameworkConfig(
            redis_host=self._env.str("REDIS_HOST", "localhost"),
            redis_port=self._env.int("REDIS_PORT", 6379),
        )


class AppBinding:
    business: BusinessFactory
    adapters: AdaptersFactory
    frameworks: FrameworksFactory

    def __init__(self, frameworks_config: FrameworksConfig) -> None:
        self.frameworks_config = frameworks_config

    def bind_frameworks(self) -> None:
        self.frameworks = FrameworksFactory(self.frameworks_config)

    def bind_adapters(self) -> None:
        self.adapters = AdaptersFactory(self.frameworks)

    def bind_business(self) -> None:
        self.business = BusinessFactory(self.adapters)

    def bind_controllers(self) -> None:
        authentication_framework = self.frameworks.authentication_provider()
        bind_controller_dependencies(self.business, authentication_framework)

    def facade(self) -> None:
        self.bind_frameworks()
        self.bind_adapters()
        self.bind_business()
        self.bind_controllers()

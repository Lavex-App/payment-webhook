import json
from typing import Any, TypedDict

from google.cloud import pubsub_v1

from payment_webhook.adapters.interface_adapters.interfaces import Event, PublisherProvider, Topic
from payment_webhook.tools import json_codec


class PubSubPublisherFrameworkConfig(TypedDict):
    credentials: str | None
    project_id: str


class PubSubPublisherManager(PublisherProvider):
    def __init__(self, config: PubSubPublisherFrameworkConfig):
        self.__project_id = config.get("project_id")
        self.__credentials = config.get("credentials")
        self.__publisher = self.__get_app()

    def publish(self, topic: Topic, event: Event, tries: int = 2) -> Any:
        topic_path = self.__publisher.topic_path(self.__project_id, topic)
        json_data = json.dumps(event.model_dump(), cls=json_codec.Encoder, default=str)
        for _ in range(tries):
            try:
                result = self.__do_publish(topic_path, json_data)
            except RuntimeError:
                ...
            else:
                return result
        raise PublishError(f"Error to publish message to topic: {topic}")

    def __do_publish(self, topic_path: str, data: str) -> Any:
        future = self.__publisher.publish(topic_path, bytes(data, "utf-8"))
        return future.result()

    def __get_app(self) -> pubsub_v1.PublisherClient:
        if self.__credentials is not None:
            return pubsub_v1.PublisherClient.from_service_account_file(self.__credentials)
        return pubsub_v1.PublisherClient()


class PublishError(RuntimeError):
    """Exception for Publisher classes."""

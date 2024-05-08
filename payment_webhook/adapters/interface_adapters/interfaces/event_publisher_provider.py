from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EventType(str, Enum):
    PAYMENT_RECEIVED = "payment-received"


class Topic(str, Enum):
    PAYMENT_RECEIVED = "tpc-payment-received"


class Event(BaseModel):
    transaction_id: str = Field(
        ...,
        title="Event ID",
        description="It provides a mean to track and manage its lifecycle",
        examples=["10c5e6c1-4d81-48d6-ab1e-02319fc57fc4"],
    )
    event_id: str = Field(
        ...,
        title="Event ID",
        description="Unique identifier for the event",
        examples=["10c5e6c1-4d81-48d6-ab1e-02319fc57fc4"],
    )
    event_type: str = Field(
        ...,
        title="Event Type",
        description="Type of the event",
        examples=["user-signup", "user-accountDelete", "payment-issued", "payment-received"],
    )
    event_datetime: str = Field(
        ...,
        title="Event Datetime",
        description="It is the timestamp indicating when an event occurred",
        examples=["2024-05-08"],
    )
    payload: dict[str, str] = Field(
        ...,
        title="Payload",
        description="Data payload of the event",
        examples=[
            {
                "txid": "f0fb163a-9f7b-4cf3-8b02-dba2578f862c",
                "payment_time": "2024-05-08",
                "uid": "c156db50-b44c-471d-927c-78f56edfcf7b",
            }
        ],
    )


class PublisherProvider(metaclass=ABCMeta):
    @abstractmethod
    def publish(self, topic: Topic, event: Event, tries: int = 2) -> Any: ...

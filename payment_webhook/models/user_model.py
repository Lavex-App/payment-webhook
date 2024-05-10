from enum import Enum

from pydantic import BaseModel


class AuthenticatedUserModel(BaseModel):
    uid: str


class PayingUserModel(AuthenticatedUserModel):
    txid: str
    payment_time: str


class ClientConnectionStatus(str, Enum):
    WAITING_FOR_PAYMENT_CONFIRMATION = "waiting4payment_confirmation"
    PAID = "paid"

    @classmethod
    def from_value(cls, value: str) -> "ClientConnectionStatus":
        match value:
            case cls.WAITING_FOR_PAYMENT_CONFIRMATION.value:
                return cls.WAITING_FOR_PAYMENT_CONFIRMATION
            case cls.PAID.value:
                return cls.PAID
            case _:
                return cls.WAITING_FOR_PAYMENT_CONFIRMATION


class ConnectedClientModel(AuthenticatedUserModel):
    status: ClientConnectionStatus

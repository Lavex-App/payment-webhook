from pydantic import BaseModel


class AuthenticatedUserModel(BaseModel):
    uid: str


class PayingUser(AuthenticatedUserModel):
    txid: str
    payment_time: str

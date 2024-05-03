from pydantic import BaseModel


class AuthenticatedUserModel(BaseModel):
    uid: str

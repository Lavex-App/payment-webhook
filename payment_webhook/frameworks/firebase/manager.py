from typing import TypedDict

import firebase_admin
import firebase_admin.auth
from fastapi import status
from fastapi.exceptions import HTTPException
from firebase_admin import credentials

from payment_webhook.adapters.interface_adapters.interfaces import AuthenticationProvider, BearerToken, UserUid


class FirebaseFrameworkConfig(TypedDict):
    credentials: str | None
    auth_app_options: dict[str, str]


class FirebaseManager(AuthenticationProvider):
    def __init__(self, config: FirebaseFrameworkConfig) -> None:
        credential = config.get("credentials")
        app_options = config.get("auth_app_options")
        if credential is None:
            self.__firebase_app = firebase_admin.initialize_app()
        else:
            self.__firebase_app = firebase_admin.initialize_app(
                credentials.Certificate(credential), options=app_options
            )

    def authenticate_by_token(self, token: BearerToken) -> UserUid:
        try:
            decoded_token = firebase_admin.auth.verify_id_token(token, self.__firebase_app)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication",
                headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            ) from error

        uid = decoded_token["uid"]
        return UserUid(uid)

from abc import ABCMeta
from typing import Annotated, Any

from fastapi import Query, status
from fastapi.exceptions import HTTPException

from payment_webhook.adapters.interface_adapters.interfaces import AuthenticationProvider, BearerToken
from payment_webhook.business.__factory__ import BusinessFactory
from payment_webhook.business.use_case import (
    CancelPaymentReceiptCheckUseCase,
    CheckPaymentOfClientInTheQueueUseCase,
    PaymentReceivedUseCase,
    SaveClientInWaitingQueueUseCase,
)


def bind_controller_dependencies(
    business_factory: BusinessFactory, authentication_service: AuthenticationProvider
) -> None:
    _ControllerDependencyManager(business_factory, authentication_service)


class ControllerDependencyManagerIsNotInitializedException(RuntimeError):
    def __init__(self) -> None:
        self.type = "Dependency Manager"
        self.msg = "Something is trying to use the ControllerDependencyManager without initialize it"
        super().__init__(self.msg)


class _Singleton(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _ControllerDependencyManager(metaclass=_Singleton):
    def __init__(
        self,
        business_factory: BusinessFactory | None = None,
        authentication_service: AuthenticationProvider | None = None,
    ) -> None:
        if business_factory:
            self.__factory = business_factory
        if authentication_service:
            self.__auth = authentication_service

    def auth_service(self) -> AuthenticationProvider:
        if self.__auth:
            return self.__auth
        raise ControllerDependencyManagerIsNotInitializedException()

    def payment_received_use_case(self) -> PaymentReceivedUseCase:
        if self.__factory:
            return self.__factory.payment_received_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()

    def save_client_in_waiting_queue_use_case(self) -> SaveClientInWaitingQueueUseCase:
        if self.__factory:
            return self.__factory.save_client_in_waiting_queue_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()

    def check_payment_of_client_in_the_queue_use_case(self) -> CheckPaymentOfClientInTheQueueUseCase:
        if self.__factory:
            return self.__factory.check_payment_of_client_in_the_queue_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()

    def cancel_payment_receipt_check_use_case(self) -> CancelPaymentReceiptCheckUseCase:
        if self.__factory:
            return self.__factory.cancel_payment_receipt_check_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()


class _ControllerDependency(metaclass=ABCMeta):
    def __init__(self, credential: Annotated[str | None, Query()]) -> None:
        if credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authentication is needed",
                headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
            )
        self._dependency_manager = _ControllerDependencyManager()
        auth = self._dependency_manager.auth_service()
        bearer_token = BearerToken(credential)
        self.uid = auth.authenticate_by_token(bearer_token)


class Waiting2ReceivePaymentControllerDependencies(_ControllerDependency):
    @property
    def save_clients_in_waiting_queue_use_case(self) -> SaveClientInWaitingQueueUseCase:
        return self._dependency_manager.save_client_in_waiting_queue_use_case()

    @property
    def check_payment_of_client_in_the_queue_use_case(self) -> CheckPaymentOfClientInTheQueueUseCase:
        return self._dependency_manager.check_payment_of_client_in_the_queue_use_case()

    @property
    def cancel_payment_receipt_check_use_case(self) -> CancelPaymentReceiptCheckUseCase:
        return self._dependency_manager.cancel_payment_receipt_check_use_case()


class PixStatusChangeReceiverControllerDependencies:
    def __init__(self) -> None:
        dependency_manager = _ControllerDependencyManager()
        self.payment_received_use_case: PaymentReceivedUseCase = dependency_manager.payment_received_use_case()

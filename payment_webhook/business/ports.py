from payment_webhook.models.user_model import AuthenticatedUserModel

from .interfaces import InputPort, OutputPort


class ExampleInputPort(AuthenticatedUserModel, InputPort): ...


class ExampleOutputPort(OutputPort):
    msg: str

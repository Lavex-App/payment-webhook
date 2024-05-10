from payment_webhook.models.user_model import AuthenticatedUserModel, ConnectedClientModel

from .interfaces import InputPort, OutputPort


class PaymentReceivedInputPort(InputPort):
    txid: str
    payment_time: str


class PaymentReceivedOutputPort(OutputPort):
    msg: str


class SaveClientInWaitingQueueInputPort(AuthenticatedUserModel, InputPort): ...


class SaveClientInWaitingQueueOutputPort(OutputPort):
    msg: str


class CheckPaymentOfClientInTheQueueInputPort(AuthenticatedUserModel, InputPort): ...


class CheckPaymentOfClientInTheQueueOutputPort(ConnectedClientModel, OutputPort):
    msg: str


class CancelPaymentReceiptCheckInputPort(AuthenticatedUserModel, OutputPort): ...


class CancelPaymentReceiptCheckOutputPort(OutputPort):
    msg: str

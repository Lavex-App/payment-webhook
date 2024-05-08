from .interfaces import InputPort, OutputPort


class PaymentReceivedInputPort(InputPort):
    txid: str
    payment_time: str


class PaymentReceivedOutputPort(OutputPort):
    msg: str

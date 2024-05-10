from fastapi.applications import FastAPI

from .pix_webhook_controller import pix_webhook_controller
from .pix_websocket_controller import pix_websocket_controller


class Binding:
    def register_all(self, app: FastAPI) -> None:
        app.include_router(pix_websocket_controller)
        app.include_router(pix_webhook_controller)

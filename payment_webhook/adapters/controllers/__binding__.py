from fastapi.applications import FastAPI

from .pix_webhook_controller import pix_webhook_controller


class Binding:
    def register_all(self, app: FastAPI) -> None:
        app.include_router(pix_webhook_controller)

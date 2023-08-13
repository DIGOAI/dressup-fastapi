from fastapi import FastAPI

from app.api.v1 import router as api_v1_router
from app.api.v1.orders import router as api_orders_router
from app.api.v1.users import router as api_users_router
from app.config import Config

Config.load_config()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_v1_router)
    app.include_router(api_orders_router)
    app.include_router(api_users_router)
    return app


app: FastAPI = create_app()

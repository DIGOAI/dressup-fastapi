from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import router as api_v1_router
from app.exeptions import SupabaseException

# from app.api.v1.orders import router as api_orders_router
# from app.api.v1.users import router as api_users_router
# from app.config import Config


def load_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(SupabaseException)
    async def supabase_exception_handler(request: Request, exc: SupabaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.name, "message": exc.message},
        )


def create_app() -> FastAPI:
    app = FastAPI()
    load_exception_handlers(app)  # Load exception handlers

    # Load routers
    app.include_router(api_v1_router)
    # app.include_router(api_orders_router)
    # app.include_router(api_users_router)
    return app


app: FastAPI = create_app()

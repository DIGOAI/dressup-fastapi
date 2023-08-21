from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.v1 import router as api_v1_router
from app.exeptions import SupabaseException

# from app.api.v1.orders import router as api_orders_router
# from app.api.v1.users import router as api_users_router
# from app.config import Config

ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://localhost:3000",
    "https://localhost:8000",
    "https://*.vercel.app",
    "https://dressup-frontend-next.vercel.app"
]


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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.get("/")
    def index():
        return RedirectResponse(url="/api/v1")

    # Load routers
    app.include_router(api_v1_router, prefix="/api")
    # app.include_router(api_orders_router)
    # app.include_router(api_users_router)
    return app


app: FastAPI = create_app()

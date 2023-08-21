from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.v1 import router as api_v1_router
from app.exeptions import SupabaseException

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

    @app.get("/", tags=["Default"], include_in_schema=False)
    def index():
        return RedirectResponse(url="/api/v1")

    app.include_router(api_v1_router, prefix="/api")
    return app


app: FastAPI = create_app()

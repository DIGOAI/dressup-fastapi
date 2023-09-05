from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1 import router as api_v1_router
from app.exeptions import SupabaseException

from app.config import Config

ORIGINS = Config.ALLOWED_ORIGINS

# Regex for this origins: http://localhost:XXXX, https://localhost:XXXX, https://*.vercel.app
# origins_pattern = r"^https?:\/\/localhost:\d{4}$|^https?:\/\/.*\.vercel\.app$"


def load_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(SupabaseException)
    async def supabase_exception_handler(request: Request, exc: SupabaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.name, "message": exc.message},
        )


def create_app() -> FastAPI:
    app = FastAPI(title="DressUp API - DIGO", version="1.5.3",
                  description="This is the API for the DressUp project.", docs_url=None)

    app.mount("/static", StaticFiles(directory="static"), name="static")

    load_exception_handlers(app)  # Load exception handlers
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.get("/docs", include_in_schema=False)
    async def swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="FastAPI",
            swagger_favicon_url="/static/favicon.png"
        )

    @app.get("/", tags=["Default"], include_in_schema=False)
    def index():
        return RedirectResponse(url="/api/v1")

    app.include_router(api_v1_router, prefix="/api")
    return app


app: FastAPI = create_app()

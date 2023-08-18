from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.keys import keys_router
from app.api.v1.models import model_router

from app.config import Config

router = APIRouter(prefix="/v1")


@router.get("/", tags=["root"])
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to the dressup backend!"}


@router.get("/ping", tags=["root"])
def ping():
    """Ping endpoint"""
    return {"message": "ok"}


router.include_router(auth_router, include_in_schema=Config.DEBUG)
router.include_router(keys_router)
router.include_router(model_router)

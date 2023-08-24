from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.keys import keys_router
from app.api.v1.models import model_router
from app.api.v1.orders import order_router
from app.api.v1.pose_sets import pose_sets_router
from app.api.v1.poses import pose_router
from app.api.v1.users import user_router
from app.config import Config

router = APIRouter(prefix="/v1")


@router.get("/", tags=["Default"])
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to the dressup backend!"}


@router.get("/ping", tags=["Default"])
def ping():
    """Ping endpoint"""
    return {"message": "ok"}


router.include_router(auth_router, include_in_schema=Config.DEBUG)
router.include_router(keys_router, include_in_schema=False)
router.include_router(order_router)
router.include_router(model_router)
router.include_router(pose_router)
router.include_router(pose_sets_router)
router.include_router(user_router)

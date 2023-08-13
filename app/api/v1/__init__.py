from fastapi import APIRouter

router = APIRouter(prefix="")

@router.get("/", tags=["root"])
async def read_root() -> dict:
    """Root endpoint"""
    return {"message": "Welcome to the dressup backend!"}
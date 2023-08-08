from fastapi import APIRouter, Depends, Header
from model import OrderSchema
from app.middlewares.auth_bearer import JWTBearer
from app.middlewares import verify_api_key

router = APIRouter()
orders = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

@router.get("/orders", tags=["orders"])
async def get_orders() -> dict:
    """Get all orders"""
    return { "data": orders }

@router.post("/orders", dependencies=[Depends(JWTBearer())], tags=["orders"])
async def add_post(order: OrderSchema, x_api_key: str = Header(...)) -> dict:
    """Adds a new order"""
    verify_api_key(x_api_key)
    order.id = len(orders) + 1
    orders.append(order.dict())
    return {
        "data": "order added."
    }

from fastapi import APIRouter, Body, Depends, Request

from app.middlewares import JWTBearer
from app.repositories import supabase
from app.schemas import OrderInsert

router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(JWTBearer())])


@router.get("/")
def get_orders(request: Request):
    user_id = request.state.user
    role = request.state.role
    print(user_id)
    return supabase.table("orders").select("*").eq("user_id", user_id).execute()


@router.post("/new")
def create_order(request: Request, order: OrderInsert = Body(...)):
    user_id = request.state.user
    role = request.state.role

    return supabase.table("orders").insert(json={
        **order.model_dump(),
        "user_id": user_id,
    }).execute()

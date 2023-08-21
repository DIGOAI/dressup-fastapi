from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from typing_extensions import TypedDict

from app.middlewares import JWTBearer
from app.repositories import supabase
from app.schemas import Order, OrderInsert, OrderWithData

router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(JWTBearer())])

OrderResponse = TypedDict("OrderResponse", {"data": Order, "count": int})
OrdersResponse = TypedDict(
    "OrdersResponse", {"data": list[Order], "count": int})
OrderWithDataResponse = TypedDict("OrderWithDataResponse", {
                                  "data": OrderWithData, "count": int})
OrdersWithDataResponse = TypedDict("OrdersWithDataResponse", {
                                   "data": list[OrderWithData], "count": int})


@router.get("/")
def get_orders(request: Request) -> OrdersResponse:
    user_id = request.state.user

    orders_res = supabase.table("orders").select(
        "*").eq("user_id", user_id).execute()

    orders = [Order(**order) for order in orders_res.data]

    return {"data": orders, "count": len(orders)}


@router.get("/{order_id}")
def get_order(request: Request, order_id: int) -> OrderResponse:
    user_id = request.state.user

    print("Order ID", order_id)

    order_res = supabase.table("orders").select(
        "*").eq("user_id", user_id).eq("id", order_id).execute()

    if len(order_res.data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order {order_id} not found.")

    order = Order(**order_res.data[0])

    return {"data": order, "count": 1}


@router.get("/with-data")
def get_orders_with_data(request: Request) -> OrdersWithDataResponse:
    user_id = request.state.user

    orders_res = supabase.table("orders").select(
        "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*)))"
    ).eq("user_id", user_id).execute()

    print(orders_res.data)

    orders = [OrderWithData(**order) for order in orders_res.data]

    return {"data": orders, "count": len(orders)}


@router.get("/{order_id}/with-data")
def get_order_with_data(request: Request, order_id: int) -> OrderWithDataResponse:
    user_id = request.state.user

    print("Order ID", order_id)

    order_res = supabase.table("orders").select(
        "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*)))"
    ).eq("user_id", user_id).eq("id", order_id).execute()

    if len(order_res.data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order {order_id} not found.")

    order = OrderWithData(**order_res.data[0])

    return {"data": order, "count": 1}


@router.post("/new")
def create_order(request: Request, order: OrderInsert = Body(...)) -> OrderResponse:
    user_id = request.state.user
    role = request.state.role

    order_res = supabase.table("orders").insert(json={
        **order.model_dump(),
        "user_id": user_id,
    }).execute()

    order_created = Order(**order_res.data[0])

    return {"data": order_created, "count": 1}

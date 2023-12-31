from datetime import date, timedelta
from typing import Any, cast

from fastapi import (APIRouter, Body, Depends, Form, HTTPException, Request,
                     UploadFile, status)
from typing_extensions import TypedDict

from app.common import (StorageFolder, upload_images_to_storage,
                        upload_images_to_storage_pil)
from app.config import Config
from app.middlewares import APITokenAuth, JWTBearer
from app.repositories import supabase
from app.schemas import (Image, Order, OrderCompleteRaw, OrderInsert,
                         OrderResume, OrderStatus, OrderUpdateStatus,
                         OrderWithData)
from app.services import dressupService
from app.utils.images import base64_to_image

router = APIRouter(prefix="/orders", tags=["Orders"])

OrderResponse = TypedDict("OrderResponse", {"data": Order, "count": int})
OrdersResponse = TypedDict(
    "OrdersResponse", {"data": list[Order], "count": int})
OrderWithDataResponse = TypedDict("OrderWithDataResponse", {
                                  "data": OrderWithData, "count": int})
OrdersWithDataResponse = TypedDict("OrdersWithDataResponse", {
                                   "data": list[OrderWithData], "count": int})

OrderResumeValues = TypedDict("OrderResumeValues", {
                              "total": int, "completed": int, "waiting": int, "in_process": int, "cancelled": int, "cost": float})
OrdersResumeResponse = TypedDict("OrdersResumeResponse", {
    "data": OrderResumeValues
})


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_orders_with_data(request: Request, start: int | None = None, end: int | None = None) -> OrdersWithDataResponse:
    user_id = request.state.user
    role = cast(str, request.state.role)

    if role.lower() == "admin" or role.lower() == "service":
        query = supabase.table("orders").select(
            "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))),items:order_items(*,img:images(*))"
        )
    else:
        query = supabase.table("orders").select(
            "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))),items:order_items(*,img:images(*))"
        ).eq("user_id", user_id)

    if start is not None and end is not None:
        print(f"Start: {start}, End: {end}")
        query = query.range(start, end)

    orders_res = query.execute()

    orders = [OrderWithData(**order) for order in orders_res.data]

    return {"data": orders, "count": len(orders)}


@router.get("/resume", dependencies=[Depends(JWTBearer())])
def get_orders_resume(request: Request, start: date | None = None, end: date | None = None) -> OrdersResumeResponse:
    user_id = request.state.user

    query = supabase.table("orders").select(
        "id,status,created_at"
    ).eq("user_id", user_id).neq("status", "FAILED")

    start = start or date.today().replace(day=1)
    end = end or date.today() + timedelta(days=1)

    print(f"Start: {start}, End: {end}")

    orders_res = query.execute()

    orders = [OrderResume(**order) for order in orders_res.data]

    total = len(orders)
    completed = len(
        [order for order in orders if order.status == OrderStatus.COMPLETED])
    waiting = len(
        [order for order in orders if order.status == OrderStatus.WAITING])
    in_process = len(
        [order for order in orders if order.status == OrderStatus.IN_PROCESS])
    cancelled = len(
        [order for order in orders if order.status == OrderStatus.CANCELLED])

    cost = completed * Config.ORDER_COST

    return {"data": {"total": total, "completed": completed, "waiting": waiting, "in_process": in_process, "cancelled": cancelled, "cost": cost}}


@router.get("/{order_id}", dependencies=[Depends(JWTBearer())])
def get_order_with_data(request: Request, order_id: int) -> OrderWithDataResponse:
    user_id = request.state.user
    role = cast(str, request.state.role)

    if role.lower() == "admin" or role.lower() == "service":
        order_res = supabase.table("orders").select(
            "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))),items:order_items(*,img:images(*))"
        ).eq("id", order_id).execute()
    else:
        order_res = supabase.table("orders").select(
            "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))),items:order_items(*,img:images(*))"
        ).eq("user_id", user_id).eq("id", order_id).execute()

    if len(order_res.data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order {order_id} not found.")

    order = OrderWithData(**order_res.data[0])

    return {"data": order, "count": 1}


@router.get("/{order_id}/service", dependencies=[Depends(APITokenAuth())])
def get_order_with_data_service(request: Request, order_id: int) -> OrderWithDataResponse:
    order_res = supabase.table("orders").select(
        "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))),items:order_items(*,img:images(*))"
    ).eq("id", order_id).execute()

    if len(order_res.data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order {order_id} not found.")

    order = OrderWithData(**order_res.data[0])

    return {"data": order, "count": 1}


@router.post("/{order_id}/update-status", dependencies=[Depends(APITokenAuth())])
def update_order_status(request: Request, order_id: int, new_status: OrderUpdateStatus = Body(...)) -> OrderResponse:
    user_id = request.state.user
    role = cast(str, request.state.role)

    if role.lower() != "admin" and role.lower() != "service":
        order_res = supabase.table("orders").select("*").eq(
            "user_id", user_id).eq("id", order_id).execute()
    else:
        order_res = supabase.table("orders").select("*").eq(
            "id", order_id).execute()

    if len(order_res.data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order {order_id} not found.")

    order = Order(**order_res.data[0])

    new_data: dict[str, Any] = {
        "status": new_status.status,
    }

    if new_status.metadata:
        new_data["metadata"] = new_status.metadata

    order_res = supabase.table("orders").update(
        json=new_data).eq("id", order.id).execute()

    order_updated = Order(**order_res.data[0])

    return {"data": order_updated, "count": 1}


@router.post("/{order_id}/complete", dependencies=[Depends(APITokenAuth())])
def complete_order(request: Request, order_id: int, completed_order: OrderCompleteRaw = Body(...)) -> OrderResponse:
    order_res = supabase.table("orders").select("*").eq(
        "id", order_id).execute()

    if len(order_res.data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order {order_id} not found.")

    images = [base64_to_image(image) for image in completed_order.images]

    inserted_images = [image.model_dump() for image in upload_images_to_storage_pil(
        images, StorageFolder.OUTPUTS)]

    images_res = supabase.table("images").insert(
        json=inserted_images).execute()

    images_t: list[Image] = [Image(**image) for image in images_res.data]

    order_images_res = supabase.table("order_items").insert(json=[{
        "order_id": order_id,
        "img": image.id,
        "type": image.type
    } for image in images_t]).execute()

    order_res = supabase.table("orders").update(json={
        "status": completed_order.status,
        "metadata": completed_order.metadata or None
    }).eq("id", order_id).execute()

    order_updated = Order(**order_res.data[0])

    return {"data": order_updated, "count": 1}


@router.post("/new", dependencies=[Depends(JWTBearer())])
def create_order(request: Request, img_front: UploadFile, img_back: UploadFile, img_left: UploadFile, img_right: UploadFile, model: int = Form(), pose_set: int = Form(), name: str = Form()) -> OrderResponse:
    user_id = request.state.user
    role = request.state.role

    inserted_images = [image.model_dump() for image in upload_images_to_storage(
        [img_front, img_back, img_left, img_right], StorageFolder.INPUTS)]

    inserted_images[0]["metadata"] = {"side": "front"}
    inserted_images[1]["metadata"] = {"side": "back"}
    inserted_images[2]["metadata"] = {"side": "left"}
    inserted_images[3]["metadata"] = {"side": "right"}

    images_res = supabase.table("images").insert(
        json=inserted_images).execute()

    images_t: list[Image] = [Image(**image) for image in images_res.data]

    order = OrderInsert(model=model, pose_set=pose_set, name=name)

    order_res = supabase.table("orders").insert(json={
        **order.model_dump(),
        "user_id": user_id,
    }).execute()

    order_created = Order(**order_res.data[0])

    order_images_res = supabase.table("order_items").insert(json=[{
        "order_id": order_created.id,
        "img": image.id
    } for image in images_t]).execute()

    # Retrieve order created with images
    order_res = supabase.table("orders").select(
        "*,model:models(*,images(*)),pose_set:pose_sets(*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))),items:order_items(*,img:images(*))"
    ).eq("id", order_created.id).execute()

    order_created_with_data = OrderWithData(**order_res.data[0])

    runpod_res = dressupService.wakeup(order_created_with_data)

    if runpod_res:
        print("Runpod Response:", runpod_res)
        supabase.table("orders").update(json={
            "process_id": runpod_res.id
        }).eq("id", order_created.id).execute()

    return {"data": order_created, "count": 1}

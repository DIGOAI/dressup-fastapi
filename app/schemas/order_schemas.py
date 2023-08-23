from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_serializer

from app.schemas.model_schemas import ModelWithImages
from app.schemas.pose_schemas import PoseSetWithPoses
from app.schemas.images_schemas import ImageInsert, Image
from app.utils.patterns import UUIDV4_PATTERN


class OrderType(str, Enum):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'


class OrderStatus(str, Enum):
    WAITING = 'WAITING'
    IN_PROCESS = 'IN_PROCESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    FAILED = 'FAILED'


class OrderBase(BaseModel):
    model: int = Field(gt=0)
    pose_set: int = Field(gt=0)


class OrderInsert(OrderBase):
    status: Optional[OrderStatus] = Field(default=OrderStatus.WAITING)
    name: Optional[str] = Field(min_length=3, max_length=255)
    metadata: Optional[Dict[str, Any]] = Field(default={})


class OrderUpdateStatus(BaseModel):
    status: OrderStatus = Field(default=OrderStatus.COMPLETED)
    process_id: Optional[str] = Field(max_length=100)


class OrderComplete(BaseModel):
    order_id: int = Field(gt=0)
    metadata: Optional[Dict[str, Any]] = Field(default={})
    images: list[ImageInsert] = Field(...)
    status: OrderStatus = Field(...)


class Order(OrderBase):
    id: int = Field(...)
    user_id: str = Field(pattern=UUIDV4_PATTERN)
    status: OrderStatus = Field(...)
    created_at: datetime = Field(...)
    name: Optional[str] = Field(...)
    process_id: Optional[str] = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore


class OrderItemBase(BaseModel):
    order_id: int = Field(gt=0)
    img: int = Field(gt=0)


class OrderItemInsert(OrderItemBase):
    type: Optional[OrderType] = Field(default=OrderType.INPUT)


class OrderItem(OrderItemBase):
    item_id: str = Field(pattern=UUIDV4_PATTERN)
    type: OrderType = Field(...)


class OrderItemWithData(OrderItem):
    img: Image


class OrderWithData(Order):
    model: ModelWithImages
    pose_set: PoseSetWithPoses
    items: list[OrderItemWithData]


class OrderResume():
    id: int = Field(gt=0)
    status: OrderStatus = Field(...)
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore

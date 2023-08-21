from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from app.schemas.model_schemas import ModelWithImages
from app.schemas.pose_schemas import PoseSetWithPoses
from app.utils.patterns import UUIDV4_PATTERN


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


class Order(OrderBase):
    id: int = Field(...)
    user_id: str = Field(pattern=UUIDV4_PATTERN)
    status: OrderStatus = Field(...)
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore


class OrderWithData(Order):
    model: ModelWithImages
    pose_set: PoseSetWithPoses

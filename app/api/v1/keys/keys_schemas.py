from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class KeyType(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    ADMIN = "ADMIN"


class KeyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    DELETED = "DELETED"


class KeyBase(BaseModel):
    model_config = ConfigDict(ser_json_timedelta='iso8601')

    name: str = Field(..., min_length=1, max_length=120)
    user_id: str = Field(...)
    type: KeyType = Field(...)
    exp: datetime = Field(...)

    @field_serializer('exp')
    def serialize_exp(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore


class KeyInsert(KeyBase):
    status: Optional[KeyStatus] = Field(default=KeyStatus.ACTIVE)


class Key(KeyBase):
    id: int = Field(...)
    status: KeyStatus = Field(...)
    key: str = Field(...)
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_exp(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore

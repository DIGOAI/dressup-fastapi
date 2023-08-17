from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class KeyType(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class KeyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    DELETED = "DELETED"


class KeyBase(BaseModel):
    model_config = ConfigDict(ser_json_timedelta='iso8601')

    name: str = Field(..., min_length=1, max_length=120)
    user_id: str = Field(...)
    type: KeyType = Field(...)


class KeyInsert(KeyBase):
    status: Optional[KeyStatus] = Field(default=KeyStatus.ACTIVE)
    exp_in: int = Field(default=0, gt=30)


class Key(KeyBase):
    id: int = Field(...)
    exp: datetime = Field(...)
    status: KeyStatus = Field(...)
    key: str = Field(...)
    created_at: datetime = Field(...)

    @field_serializer('exp', 'created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_serializer

from app.schemas.auth_schemas import UserRole, UserStatus

class Profile(BaseModel):
    id: str = Field(...)
    ruc: str = Field(...)
    names: str = Field(...)
    lastnames: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)
    role: UserRole = Field(...)
    status: UserStatus = Field(...)
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore
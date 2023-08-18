from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_serializer

from app.utils.patterns import (CI_RUC_PATTERN, PASSWORD_PATTERN,
                                PHONE_PATTERN, UUIDV4_PATTERN)


class UserRole(str, Enum):
    PUBLIC = "PUBLIC"
    USER = "USER"
    ADMIN = "ADMIN"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32,
                          pattern=PASSWORD_PATTERN)


class RegisterSchema(BaseModel):
    ruc: str = Field(min_length=10, max_length=13, pattern=CI_RUC_PATTERN)
    names: str = Field(min_length=3, max_length=80)
    lastnames: str = Field(min_length=3, max_length=80)
    email: EmailStr = Field(min_length=5, max_length=120)
    phone: str = Field(min_length=10, max_length=13, pattern=PHONE_PATTERN)
    role: Optional[UserRole] = Field(default=UserRole.USER)
    status: Optional[UserStatus] = Field(default=UserStatus.ACTIVE)
    password: str = Field(min_length=8, max_length=32,
                          pattern=PASSWORD_PATTERN)


class Profile(BaseModel):
    id: str = Field(pattern=UUIDV4_PATTERN)
    ruc: str = Field(min_length=10, max_length=13, pattern=CI_RUC_PATTERN)
    names: str = Field(min_length=3, max_length=80)
    lastnames: str = Field(min_length=3, max_length=80)
    email: EmailStr = Field(min_length=5, max_length=120)
    phone: str = Field(min_length=10, max_length=13, pattern=PHONE_PATTERN)
    role: UserRole = Field(...)
    status: UserStatus = Field(...)
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore

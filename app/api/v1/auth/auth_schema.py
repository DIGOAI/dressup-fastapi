from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

PASSWORD_PATTERN = r"^[a-zA-Z0-9_@.-]{8,32}$"
CI_RUC_PATTERN = r"^(0[1-9]|1\d|2[1-4])\d{8}(001)?$"
PHONE_PATTERN = r"^(09|\+5939)\d{8}$"


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

from pydantic import BaseModel, EmailStr, Field


PASSWORD_PATTERN = r"^[a-zA-Z0-9_@.-]{8,32}$"


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32,
                          pattern=PASSWORD_PATTERN)


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32,
                          pattern=PASSWORD_PATTERN)

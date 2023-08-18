from datetime import datetime
from typing import Annotated, Optional, Type

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, HttpUrl, field_serializer

from app.schemas import Image


class ModelBase(BaseModel):
    name: str = Field(
        examples=["Alexandra", "Maria", "Sofia", "Martina", "Laura"])


class ModelInsert(ModelBase):
    tensor_file_url: Optional[HttpUrl] = Field(
        examples=["https://example.com/tensor_file_url"])

    @classmethod
    def as_form(
        cls: Type[BaseModel],
        name: str = Form(...),
        tensor_file_url: Optional[HttpUrl] = Form(None),
    ) -> BaseModel:
        """Returns a new pydantic model with all fields as Form fields."""
        return cls(name=name, tensor_file_url=tensor_file_url)


class Model(ModelBase):
    id: int = Field(examples=[1, 2, 3, 4, 5])
    tensor_file_url: Optional[HttpUrl] = Field(
        examples=["https://example.com/tensor_file_url"])
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore


class ModelWithImages(Model):
    images: list[Image] = Field(...)


class ModelInsertForm(BaseModel):
    name: Annotated[str, Form()]
    tensor_file_url: Optional[HttpUrl]
    images: list[UploadFile]

    @classmethod
    def as_form(
        cls: Type[BaseModel],
        name: str = Form(...),
        tensor_file_url: Optional[HttpUrl] = Form(None),
        images: list[UploadFile] = Form(...),
    ) -> BaseModel:
        """Returns a new pydantic model with all fields as Form fields."""
        return cls(name=name, tensor_file_url=tensor_file_url, images=images)

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, Json, field_serializer


class ImageType(str, Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    MODEL = "MODEL"
    POSE = "POSE"


class ImageBase(BaseModel):
    name: str = Field(examples=["image1", "image2",
                      "image3", "image4", "image5"])
    url: HttpUrl = Field(examples=["https://example.com/image1", "https://example.com/image2",
                         "https://example.com/image3", "https://example.com/image4", "https://example.com/image5"])

    @field_serializer('url')
    def serialize_url(v, _info):
        return v.__str__()  # type: ignore


class ImageInsert(ImageBase):
    metadata: Optional[Json] = Field(examples=[{"key1": "value1"}, {"key2": "value2"}, {
                                     "key3": "value3"}, {"key4": "value4"}, {"key5": "value5"}])
    type: Optional[ImageType] = Field(
        examples=["INPUT", "OUTPUT", "MODEL", "POSE"], default=ImageType.INPUT)


class Image(ImageBase):
    id: int = Field(...)
    metadata: Optional[Json] = Field(examples=[{"key1": "value1"}, {"key2": "value2"}, {
                                     "key3": "value3"}, {"key4": "value4"}, {"key5": "value5"}])
    type: ImageType = Field(examples=["INPUT", "OUTPUT", "MODEL", "POSE"])
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore


class ImageKey(BaseModel):
    key: str = Field(alias="Key")

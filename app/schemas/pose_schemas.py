from datetime import datetime

from pydantic import BaseModel, Field, field_serializer

from app.schemas.images_schemas import Image


class PoseBase(BaseModel):
    name: str = Field(examples=["Pose 1"])


class Pose(PoseBase):
    id: int = Field(examples=[1])
    cover_image: int = Field(examples=[1])
    skeleton_image: int = Field(examples=[2])
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore


class PoseSetBase(BaseModel):
    name: str = Field(examples=["Pose Set 1"])


class PoseSetInsert(PoseSetBase):
    poses: list[int] = Field(examples=[[1, 2, 3, 4, 5]])


class PoseSet(PoseSetBase):
    id: int = Field(examples=[1])
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore


class PoseWithImages(Pose):
    cover_image: Image = Field(...)
    skeleton_image: Image = Field(...)


class PoseSetWithPoses(PoseSet):
    poses: list[PoseWithImages] = Field(...)

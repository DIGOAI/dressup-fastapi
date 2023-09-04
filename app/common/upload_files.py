from enum import Enum
from io import BytesIO
from typing import cast
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from PIL.Image import MIME
from PIL.Image import Image as PILImage
from pydantic import HttpUrl

from app.config import Config
from app.repositories import supabase
from app.schemas import ImageInsert, ImageKey, ImageType


class StorageFolder(str, Enum):
    MODELS = "models"
    POSES = "poses"
    INPUTS = "inputs"
    OUTPUTS = "outputs"

    def __str__(self) -> str:
        return str(self.value)


def upload_images_to_storage(images: list[UploadFile], folder: StorageFolder):
    image_keys: list[ImageKey] = []
    insert_images: list[ImageInsert] = []

    for image in images:
        filename = image.filename
        ext = filename.split(".")[-1] if filename else "jpeg"

        filename = f'{uuid4()}.{ext}'

        try:
            path = f'{folder}/{filename}'
            content_type = image.content_type or "image/jpeg"

            res = supabase.storage.from_(Config.SUPABASE_BUCKET).upload(path, image.file.read(), file_options={
                "content-type": content_type
            })

            image_keys.append(ImageKey(**res.json()))

            res_public_url = supabase.storage.from_(
                Config.SUPABASE_BUCKET).get_public_url(path)

            image_type = ImageType.INPUT

            if folder == StorageFolder.OUTPUTS:
                image_type = ImageType.OUTPUT
            elif folder == StorageFolder.MODELS:
                image_type = ImageType.MODEL
            elif folder == StorageFolder.POSES:
                image_type = ImageType.POSE

            insert_images.append(ImageInsert(
                name=filename,
                url=cast(HttpUrl, res_public_url),
                type=image_type, metadata=None)
            )

        except Exception as e:
            print("[ERROR] Supabase Storage:", e)
            print("[INFO] Deleting uploaded images")

            if len(image_keys) > 0:
                supabase.storage.from_(Config.SUPABASE_BUCKET).remove(
                    [key.key.replace(f'{Config.SUPABASE_BUCKET}/', '') for key in image_keys])

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Any image could not be uploaded, possibly due to a duplicate name")

    return insert_images


def upload_images_to_storage_pil(images: list[PILImage], folder: StorageFolder):
    image_keys: list[ImageKey] = []
    insert_images: list[ImageInsert] = []

    for image in images:
        ext = (image.format or "jpg").lower()

        filename = f'{uuid4()}.{ext}'

        try:
            path = f'{folder}/{filename}'
            content_type = MIME[image.format] if image.format else "image/jpeg"

            with BytesIO() as buffer:
                image.save(buffer, format=image.format)

                res = supabase.storage.from_(Config.SUPABASE_BUCKET).upload(path, buffer.getvalue(), file_options={
                    "content-type": content_type
                })

            image_keys.append(ImageKey(**res.json()))

            res_public_url = supabase.storage.from_(
                Config.SUPABASE_BUCKET).get_public_url(path)

            image_type = ImageType.INPUT

            if folder == StorageFolder.OUTPUTS:
                image_type = ImageType.OUTPUT
            elif folder == StorageFolder.MODELS:
                image_type = ImageType.MODEL
            elif folder == StorageFolder.POSES:
                image_type = ImageType.POSE

            insert_images.append(ImageInsert(
                name=filename,
                url=cast(HttpUrl, res_public_url),
                type=image_type, metadata=None)
            )

        except Exception as e:
            print("[ERROR] Supabase Storage:", e)
            print("[INFO] Deleting uploaded images")

            if len(image_keys) > 0:
                supabase.storage.from_(Config.SUPABASE_BUCKET).remove(
                    [key.key.replace(f'{Config.SUPABASE_BUCKET}/', '') for key in image_keys])

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Any image could not be uploaded, possibly due to a duplicate name")

    return insert_images

from enum import Enum
from typing import Optional, cast
from uuid import uuid4

from fastapi import (APIRouter, Body, Depends, Form, HTTPException, Request,
                     UploadFile, status)
from pydantic import HttpUrl
from typing_extensions import TypedDict

from app.config import Config
from app.middlewares import JWTBearer, Role
from app.repositories import supabase
from app.schemas import (Image, ImageInsert, ImageKey, ImageType, Model,
                         ModelInsert, ModelWithImages)

router = APIRouter(
    prefix="/models", tags=["models"], dependencies=[Depends(JWTBearer())])

DataResponse = TypedDict(
    "DataResponse", {"data": list[ModelWithImages], "count": int})

ModelWithImagesResponse = TypedDict("ModelWithImagesResponse", {
    "data": ModelWithImages,
    "count": int
})


@router.get("/")
def get_models(request: Request) -> DataResponse:
    res = supabase.table("models").select("*,images(*)").execute()
    data = [ModelWithImages(**model) for model in res.data]

    return {"data": data, "count": len(data)}


@router.post("/new", dependencies=[Depends(JWTBearer(Role.ADMIN))])
def create_model(model: ModelInsert = Body(...)):
    return supabase.table("models").insert(json={
        **model.model_dump(),
    }).execute()


@router.post("/new/images", dependencies=[Depends(JWTBearer(Role.ADMIN))])
def create_model_with_images(images: list[UploadFile], name: str = Form(), tensor_file_url: Optional[HttpUrl] = Form(None)) -> ModelWithImagesResponse:
    model = ModelInsert(name=name, tensor_file_url=tensor_file_url)

    inserted_images = [image.model_dump() for image in upload_images(
        images, StorageFolder.MODELS)]

    images_res = supabase.table("images").insert(
        json=inserted_images).execute()

    images_t: list[Image] = [Image(**image) for image in images_res.data]

    model_res = supabase.table("models").insert(
        json={**model.model_dump()}).execute()

    model_t = Model(**model_res.data[0])

    model_images_res = supabase.table("models_images").insert(json=[{
        "model_id": model_t.id,
        "image_id": image.id
    } for image in images_t]).execute()

    model_with_images = ModelWithImages(
        **model_t.model_dump(), images=images_t)

    return {"data": model_with_images, "count": 1}


class StorageFolder(str, Enum):
    MODELS = "models"
    POSES = "poses"
    INPUTS = "inputs"
    OUTPUTS = "outputs"


def upload_images(images: list[UploadFile], folder: StorageFolder):
    imageKeys: list[ImageKey] = []
    insert_images: list[ImageInsert] = []

    for image in images:
        ext = cast(str, image.filename).split(".")[-1]

        filename = f'{uuid4()}.{ext}'

        try:
            path = f'{folder}/{filename}'
            content_type = image.content_type or "image/jpeg"

            res = supabase.storage.from_(Config.SUPABASE_BUCKET).upload(path, image.file.read(), file_options={
                "content-type": content_type
            })

            imageKeys.append(ImageKey(**res.json()))

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

            if len(imageKeys) > 0:
                supabase.storage.from_(Config.SUPABASE_BUCKET).remove(
                    [key.key.replace(f'{Config.SUPABASE_BUCKET}/', '') for key in imageKeys])

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Any image could not be uploaded, possibly due to a duplicate name")

    return insert_images

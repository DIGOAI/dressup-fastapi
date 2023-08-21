from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, UploadFile
from pydantic import HttpUrl
from typing_extensions import TypedDict

from app.common import StorageFolder, upload_images_to_storage
from app.middlewares import JWTBearer, Role
from app.repositories import supabase
from app.schemas import Image, Model, ModelInsert, ModelWithImages

router = APIRouter(
    prefix="/models", tags=["Models"], dependencies=[Depends(JWTBearer())])

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
def create_model_with_images(images: list[UploadFile], name: str = Form(), tensor_file_url: Optional[HttpUrl] = Form(None)) -> ModelWithImagesResponse:
    model = ModelInsert(name=name, tensor_file_url=tensor_file_url)

    inserted_images = [image.model_dump() for image in upload_images_to_storage(
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

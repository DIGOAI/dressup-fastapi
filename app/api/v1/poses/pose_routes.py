from fastapi import (APIRouter, Body, Depends, Form, HTTPException, Request,
                     UploadFile, status)
from pydantic import HttpUrl
from typing_extensions import TypedDict

from app.common import StorageFolder, upload_images_to_storage
from app.config import Config
from app.middlewares import JWTBearer, Role
from app.repositories import supabase
from app.schemas import Image, PoseSet, PoseSetInsert, PoseSetWithPoses

router = APIRouter(
    prefix="/poses", tags=["poses"], dependencies=[Depends(JWTBearer())])


@router.get("/")
def get_poses(request: Request):
    res = supabase.table("poses").select("*").execute()
    return {"data": res.data, "count": len(res.data)}


@router.post("/new", dependencies=[Depends(JWTBearer(Role.ADMIN))])
def create_pose(cover: UploadFile, image: UploadFile, name: str = Form()):

    inserted_images = [image.model_dump() for image in upload_images_to_storage(
        [cover, image], StorageFolder.POSES)]

    images_res = supabase.table("images").insert(
        json=inserted_images).execute()

    images_t: list[Image] = [Image(**image) for image in images_res.data]

    pose_res = supabase.table("poses").insert(json={
        "name": name,
        "cover_image": images_t[0].id,
        "skeleton_image": images_t[1].id
    }).execute()

    return {"data": pose_res.data[0], "count": len(pose_res.data)}

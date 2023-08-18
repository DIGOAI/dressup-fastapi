from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request, UploadFile, status

from pydantic import HttpUrl
from typing_extensions import TypedDict

from app.config import Config

from app.middlewares import JWTBearer

from app.repositories import supabase

router = APIRouter(
    prefix="/poses", tags=["poses"], dependencies=[Depends(JWTBearer())])


@router.get("/")
def get_poses(request: Request):
    res = supabase.table("poses").select("*").execute()
    return {"data": res.data, "count": len(res.data)}


@router.post("/new")
def create_pose(name: str = Form(...), image_url: HttpUrl = Form(...)):
    return supabase.table("poses").insert(json={
        "name": name,
        "image_url": image_url
    }).execute()

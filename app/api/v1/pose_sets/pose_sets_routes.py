from fastapi import APIRouter, Body, Depends, Request

from app.middlewares import JWTBearer, Role
from app.repositories import supabase
from app.schemas import PoseSet, PoseSetInsert, PoseSetWithPoses

router = APIRouter(
    prefix="/pose_sets", tags=["pose sets"], dependencies=[Depends(JWTBearer())])


@router.get("/")
def get_pose_sets(request: Request):
    res = supabase.table("pose_sets").select(
        "*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))").execute()

    pose_sets_with_poses = [PoseSetWithPoses(**pose_set)
                            for pose_set in res.data]

    return {"data": pose_sets_with_poses, "count": len(pose_sets_with_poses)}


@router.post("/new", dependencies=[Depends(JWTBearer(Role.ADMIN))])
def create_pose_set(new_pose_set: PoseSetInsert = Body(...)):
    pose_res = supabase.table("pose_sets").insert(
        json={"name": new_pose_set.name}).execute()

    pose_set = PoseSet(**pose_res.data[0])

    pose_set_poses_res = supabase.table("pose_sets_poses").insert(json=[
        {"set_id": pose_set.id, "pose_id": pose} for pose in new_pose_set.poses
    ]).execute()

    pose_set_with_poses_res = supabase.table("pose_sets").select(
        "*,poses(*,cover_image:images!poses_image_fkey(*),skeleton_image:images!poses_skeleton_image_fkey(*))").eq("id", pose_set.id).single().execute()

    print(pose_set_with_poses_res.data)

    pose_set_with_poses = PoseSetWithPoses(**pose_set_with_poses_res.data)

    return {"data": pose_set_with_poses, "count": 1}

from fastapi import APIRouter
from typing_extensions import TypedDict

from app.schemas import Profile

router = APIRouter(prefix="/users", tags=["Users"])

ProfileResponse = TypedDict("ProfileResponse", {"data": Profile, "count": int}) 

@router.get("/profile", dependencies=[Depends(JWTBearer())])
def get_profile():
    user_id = request.state.user

    res = supabase.table("profiles").select('*').eq("id", user_id).single().execute()

    profile = Profile(**res.data)

    return {"data": profile, "count": 1}
from typing import cast

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from typing_extensions import TypedDict

from app.exeptions import AuthApiError, SupabaseException
from app.middlewares import signJWT
from app.repositories import supabase
from app.schemas import LoginSchema, Profile, RegisterSchema

router = APIRouter(prefix="/auth", tags=["Auth"])

LoginResponse = TypedDict(
    "LoginResponse", {"user": str | UUID4, "access_token_supabase": str, "access_token_dressup": str})


@router.post("/login")
def login(signin: LoginSchema = Body(...)) -> LoginResponse:
    try:
        res = supabase.auth.sign_in_with_password(
            credentials={"email": signin.email, "password": signin.password})

        access_token_supabase = res.session.access_token if res.session is not None else ""
        user_id = res.user.id if res.user is not None else ""

        res = supabase.table("profiles").select(
            "*").eq("id", user_id).single().execute()
        user = Profile(**res.data)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        role = user.role

        keyType = 'SERVICE' if role == 'ADMIN' else 'PUBLIC'
        exp_time_sec = 31536000 if role == 'ADMIN' else 3600

        access_token, _ = signJWT(user_id, keyType=keyType,
                                  role=user.role, exp_time_sec=exp_time_sec)

        return {"user": user_id, "access_token_supabase": access_token_supabase, "access_token_dressup": access_token}
    except Exception as e:
        raise SupabaseException(cast(AuthApiError, e))


@router.post("/register")
def register(register_data: RegisterSchema = Body(...)):
    print(register_data)

    try:
        res = supabase.auth.sign_up(
            credentials={
                "email": register_data.email,
                "password": register_data.password,
                "options": {
                    "data": {
                        "ruc": register_data.ruc,
                        "names": register_data.names,
                        "lastnames": register_data.lastnames,
                        "email": register_data.email,
                        "phone": register_data.phone,
                        "role": register_data.role,
                        "status": register_data.status,
                    }
                }
            }
        )

        print(res)
        return {"message": "register success"}
    except Exception as e:
        raise SupabaseException(cast(AuthApiError, e))

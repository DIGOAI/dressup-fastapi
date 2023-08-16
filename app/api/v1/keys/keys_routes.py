from datetime import datetime

from fastapi import APIRouter, Body, HTTPException
from pydantic import UUID4
from typing_extensions import TypedDict

from app.api.v1.keys.keys_schemas import Key, KeyInsert
from app.middlewares.auth_handler import signJWT
from app.repositories.supabase import supabase

router = APIRouter(prefix="/keys", tags=["keys"])

NewKey = TypedDict("NewKey", {"data": Key})


@router.get("/")
def get_keys(user_id: UUID4):
    print(user_id)

    keys = supabase.table("keys").select(
        "id,name,type,status,exp,key,created_at").eq("user_id", user_id).neq("status", 'DELETED').execute()

    print(keys)

    return {"data": keys}


@router.post("/new")
def new_key(key: KeyInsert = Body(...)) -> NewKey:
    print(key)

    token, payload = signJWT(key.user_id, key.type, "USER", key.exp_in)

    exp = datetime.fromtimestamp(payload["exp"])
    iat = datetime.fromtimestamp(payload["iat"])

    try:
        res = supabase.table("keys").insert(json={
            **key.model_dump(exclude={"exp_in"}),
            "exp": exp.isoformat(sep='T', timespec='seconds'),
            "key": token,
            "created_at": iat.isoformat(sep='T', timespec='seconds'),
        }).execute()

        new_key = Key(**res.data[0])

        return {"data": new_key}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")

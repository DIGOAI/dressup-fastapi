from typing import cast

from fastapi import APIRouter, Body, Header
from pydantic import UUID4
from typing_extensions import TypedDict

from app.api.v1.auth.auth_exeptions import AuthApiError, SupabaseException
from app.api.v1.auth.auth_schema import LoginSchema, RegisterSchema
# from app.middlewares import verify_api_key
from app.repositories.supabase import supabase

router = APIRouter(prefix="/auth", tags=["auth"])

LoginResponse = TypedDict(
    "LoginResponse", {"user": str | UUID4, "access_token": str})


@router.post("/login")
def login(signin: LoginSchema = Body(...)) -> LoginResponse:
    try:
        res = supabase.auth.sign_in_with_password(
            credentials={"email": signin.email, "password": signin.password})

        access_token = res.session.access_token if res.session is not None else ""
        user_id = res.user.id if res.user is not None else ""

        return {"user": user_id, "access_token": access_token}
    except Exception as e:
        raise SupabaseException(cast(AuthApiError, e))


# @router.get("/logout")
# async def logout():
#     return {"message": "Logout"}


@router.post("/register")
def register(signup: RegisterSchema = Body(...)):
    print(signup)
    res = supabase.auth.sign_up(
        credentials={"email": signup.email, "password": signup.password})
    print(res)

    return {"message": "register success"}

# Supabase sign_up response
# response = {
#     'user': User(
#         id='93438df0-eb29-418b-bccf-ffe046f678aa',
#         app_metadata={'provider': 'email', 'providers': ['email']},
#         user_metadata={},
#         aud='authenticated',
#         confirmation_sent_at=datetime.datetime(
#             2023, 8, 14, 7, 8, 20, 715806, tzinfo=TzInfo(UTC)),
#         recovery_sent_at=None,
#         email_change_sent_at=None,
#         new_email=None,
#         invited_at=None,
#         action_link=None,
#         email='gahonajuanjo@gmail.com',
#         phone='',
#         created_at=datetime.datetime(
#             2023, 8, 14, 7, 8, 20, 699591, tzinfo=TzInfo(UTC)),
#         confirmed_at=None,
#         email_confirmed_at=None,
#         phone_confirmed_at=None,
#         last_sign_in_at=None,
#         role='authenticated',
#         updated_at=datetime.datetime(
#             2023, 8, 14, 7, 8, 21, 711108, tzinfo=TzInfo(UTC)),
#         identities=[
#             UserIdentity(
#                 id='93438df0-eb29-418b-bccf-ffe046f678aa',
#                 user_id='93438df0-eb29-418b-bccf-ffe046f678aa',
#                 identity_data={'email': 'gahonajuanjo@gmail.com',
#                                'sub': '93438df0-eb29-418b-bccf-ffe046f678aa'},
#                 provider='email',
#                 created_at=datetime.datetime(
#                     2023, 8, 14, 7, 8, 20, 711016, tzinfo=TzInfo(UTC)),
#                 last_sign_in_at=datetime.datetime(
#                     2023, 8, 14, 7, 8, 20, 710973, tzinfo=TzInfo(UTC)),
#                 updated_at=datetime.datetime(
#                     2023, 8, 14, 7, 8, 20, 711016, tzinfo=TzInfo(UTC))
#             )
#         ],
#         factors=None
#     ),
#     'session': None
# }


# {
#   "data": {
#     "user": {
#       "id": "93438df0-eb29-418b-bccf-ffe046f678aa",
#       "app_metadata": {
#         "provider": "email",
#         "providers": ["email"]
#       },
#       "user_metadata": {},
#       "aud": "authenticated",
#       "confirmation_sent_at": "2023-08-14T07:08:20.715806Z",
#       "recovery_sent_at": null,
#       "email_change_sent_at": null,
#       "new_email": null,
#       "invited_at": null,
#       "action_link": null,
#       "email": "gahonajuanjo@gmail.com",
#       "phone": "",
#       "created_at": "2023-08-14T07:08:20.699591Z",
#       "confirmed_at": null,
#       "email_confirmed_at": null,
#       "phone_confirmed_at": null,
#       "last_sign_in_at": null,
#       "role": "authenticated",
#       "updated_at": "2023-08-14T07:08:21.711108Z",
#       "identities": [
#         {
#           "id": "93438df0-eb29-418b-bccf-ffe046f678aa",
#           "user_id": "93438df0-eb29-418b-bccf-ffe046f678aa",
#           "identity_data": {
#             "email": "gahonajuanjo@gmail.com",
#             "sub": "93438df0-eb29-418b-bccf-ffe046f678aa"
#           },
#           "provider": "email",
#           "created_at": "2023-08-14T07:08:20.711016Z",
#           "last_sign_in_at": "2023-08-14T07:08:20.710973Z",
#           "updated_at": "2023-08-14T07:08:20.711016Z"
#         }
#       ],
#       "factors": null
#     },
#     "session": null
#   }
# }

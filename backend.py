from fastapi import FastAPI
from app.api.v1 import router as api_v1_router
from app.api.v1.orders import router as api_orders_router
from app.api.v1.users import router as api_users_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_v1_router)
    app.include_router(api_orders_router)
    app.include_router(api_users_router)
    return app


# @app.get("/posts/{id}", tags=["posts"])
# async def get_single_post(id: int) -> dict:
#     if id > len(posts):
#         return {
#             "error": "No such post with the supplied ID."
#         }

#     for post in posts:
#         if post["id"] == id:
#             return {
#                 "data": post
#             }


# @app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
# async def add_post(post: PostSchema) -> dict:
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }

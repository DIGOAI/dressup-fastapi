from fastapi import APIRouter, Body, Header
from model import UserSchema, UserLoginSchema
from app.middlewares.auth_handler import signJWT
from app.middlewares import verify_api_key

router = APIRouter()
users = []

# helpers
def check_user(data: UserLoginSchema):
    """Helper function definition"""
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# routes
@router.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...), x_api_key: str = Header(...)):
    """Create user"""
    verify_api_key(x_api_key)
    users.append(user)  # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@router.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...), x_api_key: str = Header(...)):
    """User login"""
    verify_api_key(x_api_key)
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
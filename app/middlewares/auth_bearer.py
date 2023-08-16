from enum import IntEnum

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.middlewares.auth_handler import decodeJWT


class Role(IntEnum):
    PUBLIC = 1
    USER = 2
    ADMIN = 3


class JWTBearer(HTTPBearer):
    def __init__(self, min_role: Role = Role.PUBLIC, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")

            payload = self.verify_jwt(credentials.credentials)

            if payload is None:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")

            request.state.user = payload["sub"]
            request.state.role = payload["role"]

            return {"user": payload["sub"], "role": payload["role"]}
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str):
        try:
            return decodeJWT(jwtoken)
        except:
            return None

    def verify_role(self, role: str, min_role: str):
        return Role[role] >= Role[min_role]

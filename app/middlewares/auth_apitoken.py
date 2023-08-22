from fastapi import Depends, Request
from fastapi.security import APIKeyHeader

from app.config import Config

api_key_header_auth = APIKeyHeader(name=Config.X_API_KEY_NAME, auto_error=True)


class APITokenAuth:
    async def __call__(self, request: Request, api_key: str = Depends(APIKeyHeader(name=Config.X_API_KEY_NAME, auto_error=True))):
        if api_key:
            request.state.user = "SERVICE"
            request.state.role = "SERVICE"
            return True

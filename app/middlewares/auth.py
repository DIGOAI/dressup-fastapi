from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from app.config import config


API_KEY = config.get("API_KEY", "")
api_key_header = APIKeyHeader(name="access_token", auto_error=False)


async def get_api_key(received_api_key_header: str = Security(api_key_header)):
    """Handler function to get the api key from the request header"""
    if received_api_key_header == API_KEY:
        return received_api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
    
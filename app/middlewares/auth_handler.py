import time
from typing import Any, Dict

import jwt

from app.config import Config


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, Config.JWT_SECRET,
                       algorithm=Config.JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict[str, Any] | None:
    try:
        decoded_token = jwt.decode(
            token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

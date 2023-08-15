import time
from typing import Any

import jwt
from typing_extensions import TypedDict

from app.config import Config


TokenResponse = TypedDict(
    'TokenResponse', {"access_token": str})


def signJWT(user_id: str, apiType: str, exp_time_sec: int) -> TokenResponse:
    # exp and iat in seconds since epoch (UTC) - https://www.rfc-editor.org/rfc/rfc7519#section-2
    payload = {
        "sub": user_id,
        "type": apiType,
        "exp": int(time.time()) + exp_time_sec,
        "iat": int(time.time())
    }
    token = jwt.encode(payload, Config.JWT_SECRET,
                       algorithm=Config.JWT_ALGORITHM)

    return {"access_token": token}


def decodeJWT(token: str) -> dict[str, Any] | None:
    try:
        decoded_token = jwt.decode(
            token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM], options={"require": ["exp", "iss", "sub"]})
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}

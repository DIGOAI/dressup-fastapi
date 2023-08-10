from app.config import Config
from fastapi import HTTPException, Header


def verify_api_key(x_api_key: str = Header(...)):
    """Main method definition"""
    if x_api_key != Config.X_API_KEY:
        raise HTTPException(
            status_code=401, detail="Invalid or missing X-API-KEY")

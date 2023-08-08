from decouple import config
from fastapi import APIRouter, HTTPException, Header

# helper
EXPECTED_API_KEY = config("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    """Main method definition"""
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-KEY")

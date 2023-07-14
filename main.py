from fastapi import FastAPI, Depends
from app.api.v1 import router as api_router_v1
from fastapi.security.api_key import APIKey
from app.middlewares  import auth

app = FastAPI()
app.include_router(api_router_v1)

# Lockedown Route
@app.get("/secure")
async def info(api_key: APIKey = Depends(auth.get_api_key)):
    return {
        "default variable": api_key
    }

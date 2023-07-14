from fastapi import FastAPI
from app.api.v1 import router as api_router_v1


app = FastAPI()
app.include_router(api_router_v1)


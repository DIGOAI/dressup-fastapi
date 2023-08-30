from app.config import Config
from app.utils.requests import APIRequester

DRESSUP_RUNPOD_API_URL = Config.DRESSUP_RUNPOD_API_URL
DRESSUP_RUNPOD_BEARER_TOKEN = Config.DRESSUP_RUNPOD_BEARER_TOKEN

api_client = APIRequester(DRESSUP_RUNPOD_API_URL, DRESSUP_RUNPOD_BEARER_TOKEN )


class DressUpRunpodService:
    def __init__(self):
        pass

    def wakeup(self, order: dict):
        body = {
            "input": {
                "order": order
            }
        }
        api_client.send_request(
            method="POST",
            endpoint="/",
            json=body
        )


dressupService = DressUpRunpodService()
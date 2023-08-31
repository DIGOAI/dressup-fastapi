from app.config import Config
from app.services.runpod_dressup import RunpodDressUpService

dressupService = RunpodDressUpService(
    Config.DRESSUP_RUNPOD_URL,
    Config.DRESSUP_RUNPOD_TOKEN
)

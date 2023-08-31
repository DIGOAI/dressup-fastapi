from pydantic import BaseModel, Field
from app.utils.patterns import UUIDV4_PATTERN


class RunpodResponse(BaseModel):
    id: str = Field(pattern=UUIDV4_PATTERN)
    status: str = Field(...)

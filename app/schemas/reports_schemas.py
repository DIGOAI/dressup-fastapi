from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer
from app.utils.patterns import UUIDV4_PATTERN


class ReportType(str, Enum):
    MISREPRESENTATION_OF_CONTENT = 'MISREPRESENTATION_OF_CONTENT'
    INAPPROPRIATE_CONTENT = 'INAPPROPRIATE_CONTENT'
    ACCURACY_ISSUES = 'ACCURACY_ISSUES'
    OTHER = 'OTHER'

class ReportBase(BaseModel):
    user_id: str = Field(pattern=UUIDV4_PATTERN)
    order_id: int = Field(gt=0)
    type: ReportType = Field(default=ReportType.OTHER)

class ReportInsert(ReportBase):
    description: Optional[str] = Field(min_length=3, max_length=255)


class Report(ReportBase):
    id: int = Field(...)
    created_at: datetime = Field(...)

    @field_serializer('created_at')
    def serialize_datetime(v, _info):
        return v.isoformat(sep='T', timespec='seconds')  # type: ignore
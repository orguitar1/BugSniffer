from pydantic import BaseModel
from typing import Optional
from enum import Enum


class SeverityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Finding(BaseModel):
    id: str
    title: str
    description: str

    severity: SeverityLevel

    file: str
    line: Optional[int] = None

    scanner: str
    confidence: float

    class Config:
        use_enum_values = True
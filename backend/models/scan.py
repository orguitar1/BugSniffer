from datetime import datetime

from pydantic import BaseModel
from typing import List
from backend.models.finding import Finding


class ScanRequest(BaseModel):
    repository_url: str


class ScanResponse(BaseModel):
    scan_id: str
    findings: List[Finding]


class ScanDetailResponse(BaseModel):
    scan_id: str
    repository_url: str
    status: str
    findings: List[Finding]
    created_at: datetime
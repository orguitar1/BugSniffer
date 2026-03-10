from pydantic import BaseModel
from typing import List
from backend.models.finding import Finding


class ScanRequest(BaseModel):
    repository_url: str


class ScanResponse(BaseModel):
    findings: List[Finding]
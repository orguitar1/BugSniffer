from fastapi import APIRouter
from backend.models.scan import ScanRequest, ScanResponse
from backend.services.scan_service import scan_repository

router = APIRouter()

@router.post("/scan", response_model=ScanResponse)
def scan_repo(request: ScanRequest):

    findings = scan_repository(request.repository_url)

    return ScanResponse(findings=findings)
from fastapi import APIRouter
from backend.models.scan import ScanRequest, ScanResponse

router = APIRouter()


@router.post("/scan", response_model=ScanResponse)
def run_scan(request: ScanRequest):
    # scanning logic will be added later
    return ScanResponse(findings=[])
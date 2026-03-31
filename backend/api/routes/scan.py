from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.scan import ScanRequest, ScanResponse, ScanDetailResponse
from backend.services.scan_service import scan_repository, get_scan_by_id
from backend.services.repo_service import RepoCloneError

router = APIRouter()


@router.post("/scan", response_model=ScanResponse)
def scan_repo(request: ScanRequest, db: Session = Depends(get_db)):
    try:
        return scan_repository(request.repository_url, db)

    except RepoCloneError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to clone repository: {str(e)}"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/scan/{scan_id}", response_model=ScanDetailResponse)
def get_scan(scan_id: str, db: Session = Depends(get_db)):
    result = get_scan_by_id(scan_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return result

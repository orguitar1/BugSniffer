from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.scan import ScanRequest, ScanResponse
from backend.services.scan_service import scan_repository
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

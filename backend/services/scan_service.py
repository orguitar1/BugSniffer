from typing import List
import shutil
import logging

from sqlalchemy.orm import Session

from backend.models.finding import Finding
from backend.models.scan import ScanResponse, ScanDetailResponse
from backend.models.scan_record import ScanRecord
from backend.services.repo_service import clone_repository, RepoCloneError
from scanners.registry import get_scanners

logger = logging.getLogger(__name__)


def get_scan_by_id(scan_id: str, db: Session) -> ScanDetailResponse | None:
    record = db.query(ScanRecord).filter(ScanRecord.id == scan_id).first()
    if record is None:
        return None

    findings_data = record.findings if record.findings is not None else []
    findings = [Finding(**f) for f in findings_data]

    return ScanDetailResponse(
        scan_id=record.id,
        repository_url=record.repository_url,
        status=record.status,
        findings=findings,
        created_at=record.created_at,
    )


def scan_repository(repository_url: str, db: Session) -> ScanResponse:
    logger.info(f"Scan requested for repository: {repository_url}")

    record = ScanRecord(repository_url=repository_url, status="pending")
    db.add(record)
    db.commit()

    try:
        repo_path = clone_repository(repository_url)

        findings: List[Finding] = []

        try:
            for scanner in get_scanners():
                logger.info(f"Running scanner: {scanner.name}")
                scanner_findings = scanner.scan(repo_path)
                logger.info(f"Scanner {scanner.name} returned {len(scanner_findings)} findings")
                findings.extend(scanner_findings)
        finally:
            logger.debug(f"Cleaning up temp directory: {repo_path}")
            shutil.rmtree(repo_path, ignore_errors=True)

        record.status = "complete"
        record.findings = [f.model_dump() for f in findings]
        db.commit()

        return ScanResponse(scan_id=record.id, findings=findings)

    except RepoCloneError:
        record.status = "failed"
        db.commit()
        raise

    except Exception as e:
        record.status = "failed"
        db.commit()
        logger.error(f"Error during scan: {e}", exc_info=True)
        raise

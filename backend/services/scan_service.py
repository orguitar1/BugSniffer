from typing import List
import shutil
import logging

from backend.models.finding import Finding
from backend.services.repo_service import clone_repository
from scanners.registry import get_scanners

logger = logging.getLogger(__name__)


def scan_repository(repository_url: str) -> List[Finding]:
    logger.info(f"Scan requested for repository: {repository_url}")

    repo_path = clone_repository(repository_url)

    findings: List[Finding] = []

    try:
        for scanner in get_scanners():
            logger.info(f"Running scanner: {scanner.name}")
            scanner_findings = scanner.scan(repo_path)
            logger.info(f"Scanner {scanner.name} returned {len(scanner_findings)} findings")
            findings.extend(scanner_findings)
    except Exception as e:
        logger.error(f"Error during scan: {e}", exc_info=True)
        raise
    finally:
        logger.debug(f"Cleaning up temp directory: {repo_path}")
        shutil.rmtree(repo_path, ignore_errors=True)

    return findings
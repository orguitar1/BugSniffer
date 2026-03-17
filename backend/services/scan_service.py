from typing import List
import shutil

from backend.models.finding import Finding
from backend.services.repo_service import clone_repository, RepoCloneError
from scanners.registry import get_scanners


def scan_repository(repository_url: str) -> List[Finding]:

    try:
        repo_path = clone_repository(repository_url)

    except RepoCloneError as e:
        # You have two choices here — I’ll explain below
        raise e

    findings: List[Finding] = []

    try:
        for scanner in get_scanners():
            findings.extend(scanner.scan(repo_path))
    finally:
        shutil.rmtree(repo_path, ignore_errors=True)

    return findings
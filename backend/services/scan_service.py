from typing import List
from backend.models.finding import Finding
from backend.services.repo_service import clone_repository
from scanners.bandit_scanner import run_bandit


def scan_repository(repository_url: str) -> List[Finding]:

    repo_path = clone_repository(repository_url)

    findings = []

    findings.extend(run_bandit(repo_path))

    return findings
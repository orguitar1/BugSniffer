from typing import List
from backend.models.finding import Finding


def scan_repository(repository_url: str) -> List[Finding]:
    """
    Main scan orchestration function.

    Future responsibilities:
    - clone the repository
    - run scanners
    - aggregate findings
    """

    findings: List[Finding] = []

    return findings
from typing import List

from scanners.base_scanner import BaseScanner
from scanners.bandit_scanner import BanditScanner
from scanners.semgrep_scanner import SemgrepScanner


def get_scanners() -> List[BaseScanner]:
    """
    Return all scanners that should run for a scan job.
    """

    return [
        BanditScanner(),
        SemgrepScanner(),
    ]
from typing import List

from scanners.base_scanner import BaseScanner
from scanners.bandit_scanner import BanditScanner


def get_scanners() -> List[BaseScanner]:
    """
    Return all scanners that should run for a scan job.
    """

    return [
        BanditScanner(),
    ]
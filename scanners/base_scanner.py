from abc import ABC, abstractmethod
from typing import List
from backend.models.finding import Finding


class BaseScanner(ABC):
    name: str

    @abstractmethod
    def scan(self, repo_path: str) -> List[Finding]:
        """
        Run the scanner against a repository path
        and return a list of findings.
        """
        pass
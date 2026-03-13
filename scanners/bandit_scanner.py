import subprocess
import json
from typing import List

from backend.models.finding import Finding
from scanners.base_scanner import BaseScanner


class BanditScanner(BaseScanner):

    name = "bandit"

    def scan(self, repo_path: str) -> List[Finding]:

        findings: List[Finding] = []

        try:
            result = subprocess.run(
                ["bandit", "-r", repo_path, "-f", "json"],
                capture_output=True,
                text=True
            )

            if result.stdout:
                data = json.loads(result.stdout)

                for issue in data.get("results", []):

                    finding = Finding(
                        id=issue.get("test_id"),
                        title=issue.get("issue_text"),
                        description=issue.get("issue_text"),
                        severity=issue.get("issue_severity").lower(),
                        file=issue.get("filename"),
                        line=issue.get("line_number"),
                        scanner=self.name,
                        confidence=0.9
                    )

                    findings.append(finding)

        except Exception:
            pass

        return findings
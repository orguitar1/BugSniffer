import subprocess
import json
import logging
from typing import List

from backend.models.finding import Finding
from scanners.base_scanner import BaseScanner

logger = logging.getLogger(__name__)

CONFIDENCE_MAP = {
    "LOW": 0.3,
    "MEDIUM": 0.6,
    "HIGH": 0.9,
}


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

            if not result.stdout:
                logger.warning("BanditScanner: no output from bandit subprocess")
                return findings

            data = json.loads(result.stdout)

            for issue in data.get("results", []):
                confidence_raw = issue.get("issue_confidence", "MEDIUM").upper()
                confidence = CONFIDENCE_MAP.get(confidence_raw, 0.6)

                finding = Finding(
                    id=issue.get("test_id"),
                    title=issue.get("issue_text"),
                    description=issue.get("issue_text"),
                    severity=issue.get("issue_severity").lower(),
                    file=issue.get("filename"),
                    line=issue.get("line_number"),
                    scanner=self.name,
                    confidence=confidence
                )

                findings.append(finding)

        except json.JSONDecodeError as e:
            logger.error(f"BanditScanner: failed to parse JSON output: {e}")
        except FileNotFoundError:
            logger.error("BanditScanner: bandit executable not found — is it installed?")
        except Exception as e:
            logger.exception(f"BanditScanner: unexpected error: {e}")

        return findings
import subprocess
import json
import uuid
import logging
from typing import List

from backend.models.finding import Finding, SeverityLevel
from scanners.base_scanner import BaseScanner

logger = logging.getLogger(__name__)

SEVERITY_MAP = {
    "ERROR": (SeverityLevel.high, 0.9),
    "WARNING": (SeverityLevel.medium, 0.6),
    "INFO": (SeverityLevel.low, 0.3),
}


class SemgrepScanner(BaseScanner):

    name = "semgrep"

    def scan(self, repo_path: str) -> List[Finding]:

        findings: List[Finding] = []

        try:
            result = subprocess.run(
                ["semgrep", "--config", "auto", repo_path, "--json", "--quiet"],
                capture_output=True,
                text=True,
                check=False
            )

            if not result.stdout:
                logger.warning("SemgrepScanner: no output from semgrep subprocess")
                return findings

            data = json.loads(result.stdout)

            for item in data.get("results", []):
                raw_severity = item.get("extra", {}).get("severity", "").upper()
                severity, confidence = SEVERITY_MAP.get(raw_severity, (SeverityLevel.low, 0.3))

                finding = Finding(
                    id=str(uuid.uuid4()),
                    title=item.get("check_id"),
                    description=item.get("extra", {}).get("message"),
                    severity=severity,
                    file=item.get("path"),
                    line=item.get("start", {}).get("line"),
                    scanner=self.name,
                    confidence=confidence
                )

                findings.append(finding)

        except json.JSONDecodeError as e:
            logger.error(f"SemgrepScanner: failed to parse JSON output: {e}")
        except FileNotFoundError:
            logger.error("SemgrepScanner: semgrep executable not found — is it installed?")
        except Exception as e:
            logger.exception(f"SemgrepScanner: unexpected error: {e}")

        return findings

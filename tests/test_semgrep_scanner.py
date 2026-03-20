from unittest.mock import patch, MagicMock
from subprocess import CompletedProcess
import json

from scanners.semgrep_scanner import SemgrepScanner
from backend.models.finding import Finding


def test_successful_scan_returns_findings():
    semgrep_output = {
        "results": [
            {
                "check_id": "python.lang.security.audit.exec-detected",
                "path": "app.py",
                "start": {"line": 15},
                "extra": {
                    "message": "Detected use of exec()",
                    "severity": "ERROR"
                }
            }
        ]
    }

    mock_result = CompletedProcess(
        args=["semgrep"], returncode=0,
        stdout=json.dumps(semgrep_output), stderr=""
    )

    with patch("scanners.semgrep_scanner.subprocess.run", return_value=mock_result):
        findings = SemgrepScanner().scan("/tmp/fake_repo")

    assert len(findings) == 1
    assert isinstance(findings[0], Finding)
    assert findings[0].title == "python.lang.security.audit.exec-detected"
    assert findings[0].description == "Detected use of exec()"
    assert findings[0].severity == "high"
    assert findings[0].file == "app.py"
    assert findings[0].line == 15
    assert findings[0].scanner == "semgrep"
    assert findings[0].confidence == 0.9


def test_empty_stdout_returns_empty_list():
    mock_result = CompletedProcess(
        args=["semgrep"], returncode=0,
        stdout="", stderr=""
    )

    with patch("scanners.semgrep_scanner.subprocess.run", return_value=mock_result):
        findings = SemgrepScanner().scan("/tmp/fake_repo")

    assert findings == []


def test_invalid_json_returns_empty_list():
    mock_result = CompletedProcess(
        args=["semgrep"], returncode=0,
        stdout="not valid json", stderr=""
    )

    with patch("scanners.semgrep_scanner.subprocess.run", return_value=mock_result):
        findings = SemgrepScanner().scan("/tmp/fake_repo")

    assert findings == []


def test_file_not_found_returns_empty_list():
    with patch("scanners.semgrep_scanner.subprocess.run", side_effect=FileNotFoundError):
        findings = SemgrepScanner().scan("/tmp/fake_repo")

    assert findings == []

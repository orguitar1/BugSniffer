from unittest.mock import patch
from subprocess import CompletedProcess
import json

from scanners.bandit_scanner import BanditScanner
from backend.models.finding import Finding


def test_successful_scan_returns_findings():
    bandit_output = {
        "results": [
            {
                "test_id": "B101",
                "issue_text": "Use of assert detected.",
                "issue_severity": "LOW",
                "issue_confidence": "HIGH",
                "filename": "app.py",
                "line_number": 10,
            }
        ]
    }

    mock_result = CompletedProcess(
        args=["bandit"], returncode=0,
        stdout=json.dumps(bandit_output), stderr=""
    )

    with patch("scanners.bandit_scanner.subprocess.run", return_value=mock_result):
        findings = BanditScanner().scan("/tmp/fake_repo")

    assert len(findings) == 1
    assert isinstance(findings[0], Finding)
    assert findings[0].id == "B101"
    assert findings[0].title == "Use of assert detected."
    assert findings[0].description == "Use of assert detected."
    assert findings[0].severity == "low"
    assert findings[0].confidence == 0.9
    assert findings[0].file == "app.py"
    assert findings[0].line == 10
    assert findings[0].scanner == "bandit"


def test_empty_stdout_returns_empty_list():
    mock_result = CompletedProcess(
        args=["bandit"], returncode=0,
        stdout="", stderr=""
    )

    with patch("scanners.bandit_scanner.subprocess.run", return_value=mock_result):
        findings = BanditScanner().scan("/tmp/fake_repo")

    assert findings == []


def test_invalid_json_returns_empty_list():
    mock_result = CompletedProcess(
        args=["bandit"], returncode=0,
        stdout="not valid json", stderr=""
    )

    with patch("scanners.bandit_scanner.subprocess.run", return_value=mock_result):
        findings = BanditScanner().scan("/tmp/fake_repo")

    assert findings == []


def test_file_not_found_returns_empty_list():
    with patch("scanners.bandit_scanner.subprocess.run", side_effect=FileNotFoundError):
        findings = BanditScanner().scan("/tmp/fake_repo")

    assert findings == []


def test_confidence_mapping():
    bandit_output = {
        "results": [
            {
                "test_id": "B101",
                "issue_text": "Use of assert detected.",
                "issue_severity": "LOW",
                "issue_confidence": "LOW",
                "filename": "app.py",
                "line_number": 10,
            },
            {
                "test_id": "B101",
                "issue_text": "Use of assert detected.",
                "issue_severity": "LOW",
                "issue_confidence": "MEDIUM",
                "filename": "app.py",
                "line_number": 10,
            },
            {
                "test_id": "B101",
                "issue_text": "Use of assert detected.",
                "issue_severity": "LOW",
                "issue_confidence": "HIGH",
                "filename": "app.py",
                "line_number": 10,
            },
            {
                "test_id": "B101",
                "issue_text": "Use of assert detected.",
                "issue_severity": "LOW",
                "issue_confidence": "UNDEFINED",
                "filename": "app.py",
                "line_number": 10,
            },
        ]
    }

    mock_result = CompletedProcess(
        args=["bandit"], returncode=0,
        stdout=json.dumps(bandit_output), stderr=""
    )

    with patch("scanners.bandit_scanner.subprocess.run", return_value=mock_result):
        findings = BanditScanner().scan("/tmp/fake_repo")

    assert len(findings) == 4
    assert findings[0].confidence == 0.3
    assert findings[1].confidence == 0.6
    assert findings[2].confidence == 0.9
    assert findings[3].confidence == 0.6

from unittest.mock import patch, MagicMock
from backend.services.scan_service import scan_repository
from backend.services.repo_service import RepoCloneError
from backend.models.finding import Finding, SeverityLevel
import pytest


def test_clone_failure_raises_repo_clone_error(db_session):
    with patch("backend.services.scan_service.clone_repository", side_effect=RepoCloneError("Clone failed")):
        with pytest.raises(RepoCloneError):
            scan_repository("https://github.com/invalid/repo", db_session)


def test_successful_scan_returns_scan_response(db_session):
    mock_finding = Finding(
        id="B101",
        title="Use of assert detected",
        description="Use of assert detected",
        severity=SeverityLevel.low,
        file="app.py",
        line=10,
        scanner="bandit",
        confidence=0.9
    )

    mock_scanner = MagicMock()
    mock_scanner.scan.return_value = [mock_finding]

    with patch("backend.services.scan_service.clone_repository", return_value="/tmp/fake_repo"):
        with patch("backend.services.scan_service.get_scanners", return_value=[mock_scanner]):
            with patch("backend.services.scan_service.shutil.rmtree"):
                result = scan_repository("https://github.com/some/repo", db_session)

    assert result.scan_id is not None
    assert len(result.findings) == 1
    assert result.findings[0].id == "B101"

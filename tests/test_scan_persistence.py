from unittest.mock import patch
from backend.models.finding import Finding, SeverityLevel
from backend.models.scan_record import ScanRecord


def test_successful_scan_writes_complete_record(client, db_session):
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

    with patch("backend.services.scan_service.clone_repository", return_value="/tmp/fake-repo"):
        with patch("backend.services.scan_service.get_scanners") as mock_scanners:
            mock_scanner = type("MockScanner", (), {"name": "bandit", "scan": lambda self, path: [mock_finding]})()
            mock_scanners.return_value = [mock_scanner]
            with patch("backend.services.scan_service.shutil.rmtree"):
                response = client.post("/scan", json={"repository_url": "https://github.com/some/repo"})

    assert response.status_code == 200
    data = response.json()
    assert "scan_id" in data
    assert "findings" in data

    record = db_session.query(ScanRecord).filter_by(id=data["scan_id"]).first()
    assert record is not None
    assert record.repository_url == "https://github.com/some/repo"
    assert record.status == "complete"
    assert record.findings is not None
    assert len(record.findings) > 0
    assert record.id == data["scan_id"]


def test_failed_scan_writes_failed_record(client, db_session):
    from backend.services.repo_service import RepoCloneError

    with patch("backend.services.scan_service.clone_repository", side_effect=RepoCloneError("Clone failed")):
        response = client.post("/scan", json={"repository_url": "https://github.com/invalid/repo"})

    assert response.status_code == 400

    record = db_session.query(ScanRecord).first()
    assert record is not None
    assert record.status == "failed"
    assert record.findings is None

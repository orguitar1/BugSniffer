from unittest.mock import patch, MagicMock
from backend.models.finding import Finding, SeverityLevel
from backend.models.scan import ScanResponse


def test_valid_repo_returns_200(client):
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

    mock_response = ScanResponse(scan_id="test-uuid-1234", findings=[mock_finding])

    with patch("backend.api.routes.scan.scan_repository", return_value=mock_response):
        response = client.post("/scan", json={"repository_url": "https://github.com/some/repo"})

    assert response.status_code == 200
    data = response.json()
    assert "findings" in data
    assert "scan_id" in data
    assert data["scan_id"] == "test-uuid-1234"


def test_invalid_repo_returns_400(client):
    from backend.services.repo_service import RepoCloneError

    with patch("backend.api.routes.scan.scan_repository", side_effect=RepoCloneError("Clone failed")):
        response = client.post("/scan", json={"repository_url": "https://github.com/invalid/repo"})

    assert response.status_code == 400
    assert "detail" in response.json()

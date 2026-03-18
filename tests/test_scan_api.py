from unittest.mock import patch, MagicMock
from backend.models.finding import Finding, SeverityLevel


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

    with patch("backend.api.routes.scan.scan_repository", return_value=[mock_finding]):
        response = client.post("/scan", json={"repository_url": "https://github.com/some/repo"})

    assert response.status_code == 200
    assert "findings" in response.json()


def test_invalid_repo_returns_400(client):
    from backend.services.repo_service import RepoCloneError

    with patch("backend.api.routes.scan.scan_repository", side_effect=RepoCloneError("Clone failed")):
        response = client.post("/scan", json={"repository_url": "https://github.com/invalid/repo"})

    assert response.status_code == 400
    assert "detail" in response.json()

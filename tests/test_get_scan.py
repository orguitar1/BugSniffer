from backend.models.scan_record import ScanRecord


def test_get_scan_success(client, db_session):
    record = ScanRecord(
        id="test-uuid-1234",
        repository_url="https://github.com/some/repo",
        status="complete",
        findings=[
            {
                "id": "B101",
                "title": "Use of assert detected",
                "description": "Use of assert detected",
                "severity": "low",
                "file": "app.py",
                "line": 10,
                "scanner": "bandit",
                "confidence": 0.9,
            }
        ],
    )
    db_session.add(record)
    db_session.commit()

    response = client.get("/scan/test-uuid-1234")

    assert response.status_code == 200
    data = response.json()
    assert data["scan_id"] == "test-uuid-1234"
    assert data["repository_url"] == "https://github.com/some/repo"
    assert data["status"] == "complete"
    assert len(data["findings"]) == 1
    assert data["findings"][0]["id"] == "B101"
    assert data["findings"][0]["severity"] == "low"
    assert "created_at" in data


def test_get_scan_not_found(client):
    response = client.get("/scan/nonexistent-uuid")

    assert response.status_code == 404
    assert response.json() == {"detail": "Scan not found"}


def test_get_scan_failed_status(client, db_session):
    record = ScanRecord(
        id="failed-uuid-5678",
        repository_url="https://github.com/invalid/repo",
        status="failed",
        findings=None,
    )
    db_session.add(record)
    db_session.commit()

    response = client.get("/scan/failed-uuid-5678")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "failed"
    assert data["findings"] == []


def test_get_scan_pending_status(client, db_session):
    record = ScanRecord(
        id="pending-uuid-9012",
        repository_url="https://github.com/some/repo",
        status="pending",
        findings=None,
    )
    db_session.add(record)
    db_session.commit()

    response = client.get("/scan/pending-uuid-9012")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["findings"] == []

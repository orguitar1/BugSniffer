# API Design: Scan Persistence and GET /scan/{id}

## 1. Overview

This document defines the design for adding scan persistence and a `GET /scan/{id}` endpoint to BugSniffer. The existing `POST /scan` behavior does not change — it continues to clone the repository, run scanners, and return findings. The only addition is that scan results are now persisted so they can be retrieved later by ID.

## 2. New Endpoint: GET /scan/{id}

- **Path**: `GET /scan/{id}`
- **Path parameter**: `id` (string, UUID) — the scan identifier returned by `POST /scan`
- **Success response**: HTTP 200

```json
{
  "scan_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "repository_url": "https://github.com/example/repo",
  "status": "complete",
  "findings": [
    {
      "id": "...",
      "title": "...",
      "description": "...",
      "severity": "high",
      "file": "app.py",
      "line": 15,
      "scanner": "semgrep",
      "confidence": 0.9
    }
  ],
  "created_at": "2026-03-20T14:30:00Z"
}
```

- **Error response**: HTTP 404 when the scan ID is not found

```json
{
  "detail": "Scan not found"
}
```

- No authentication is in scope for this design.

## 3. Updated Behavior: POST /scan

The existing `POST /scan` endpoint continues to accept a `ScanRequest` with `repository_url`, clone the repo, run scanners, and return findings. The change: on a successful scan, the result is persisted to the database before returning the response.

The `ScanResponse` model gains a `scan_id` field:

```json
{
  "scan_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "findings": [...]
}
```

Updated `ScanResponse` shape:

```python
class ScanResponse(BaseModel):
    scan_id: str
    findings: List[Finding]
```

Callers can use `scan_id` to retrieve the scan later via `GET /scan/{id}`.

## 4. Persistence Model

- **Storage**: SQLite via SQLAlchemy
- **Table**: `ScanRecord`

| Field           | Type     | Notes                                          |
|-----------------|----------|-------------------------------------------------|
| id              | UUID     | Primary key, generated server-side              |
| repository_url  | String   | The URL submitted in the scan request           |
| status          | String   | One of: pending, running, complete, failed      |
| findings        | JSON     | Serialized list of Finding objects              |
| created_at      | DateTime | Set automatically when the record is created    |

**Rationale**: SQLite requires no infrastructure, is easy to swap for Postgres later, and is sufficient for synchronous single-process scans at this stage.

Note on status transitions: In the current synchronous implementation, a scan transitions from pending directly to complete or failed within a single request. The running status is reserved for future async processing.

## 5. What Does Not Change

- Scanner execution (Bandit, Semgrep, registry pattern)
- Finding schema (id, title, description, severity, file, line, scanner, confidence)
- Error handling (RepoCloneError returns 400, generic exceptions return 500)
- Temp directory cleanup via try/finally
- Logging across services and scanners

## 6. Out of Scope

- Authentication
- Async scan processing
- Pagination of results
- Scan cancellation

# BugSniffer — Project State

Last Updated: 2026-03-31
Phase: Phase 2 – Scanner Integration (complete)

---

## Backend

Framework: FastAPI (Python)
Status: Full scan pipeline with two scanners, GET /scan/{id} retrieval, SQLite persistence via SQLAlchemy, logging, error handling, 19 tests, and Docker setup

---

## Frontend

Framework: React / Next.js (planned)
Status: Not implemented

---

## Implemented Components

- FastAPI application entry point with GET /health endpoint
- POST /scan endpoint accepting repository URL, returning scan_id and findings
- GET /scan/{scan_id} endpoint returning full scan details (scan_id, repository_url, status, findings, created_at) with 404 for unknown IDs
- Structured error handling in scan endpoint: RepoCloneError returns 400, generic exceptions return 500
- Database session injection via FastAPI Depends(get_db) in scan routes
- Finding Pydantic model with SeverityLevel enum (low/medium/high/critical)
- ScanRequest (repository_url), ScanResponse (scan_id, findings), and ScanDetailResponse (scan_id, repository_url, status, findings, created_at) models
- ScanRecord SQLAlchemy ORM model — scan_records table (id UUID, repository_url, status, findings JSON, created_at)
- SQLite database via SQLAlchemy 2.x (Mapped/mapped_column API, DeclarativeBase)
- Database layer: engine with check_same_thread=False, SessionLocal factory, get_db() FastAPI dependency, Base isolated in base.py to prevent circular imports
- init_db() called at app startup — creates tables idempotently via Base.metadata.create_all
- Repository cloning service via subprocess (git clone to temp dir)
- RepoCloneError custom exception with temp dir cleanup on failure
- Scan orchestration service: creates pending ScanRecord, clones repo, runs scanners, updates status to complete/failed, commits, returns ScanResponse
- Scan retrieval service: queries ScanRecord by ID, deserializes findings JSON back into Finding objects, coerces None findings to empty list, returns ScanDetailResponse
- BaseScanner ABC with abstract scan() method
- BanditScanner: runs bandit -r via subprocess, parses JSON output, maps Bandit confidence levels (LOW=0.3, MEDIUM=0.6, HIGH=0.9), logs errors
- SemgrepScanner: runs semgrep --config auto via subprocess, parses JSON output, maps severity (ERROR=high/0.9, WARNING=medium/0.6, INFO=low/0.3), logs errors
- Scanner registry pattern (get_scanners() returns [BanditScanner, SemgrepScanner])
- Logging: root logger configured in main.py (INFO level), module-level loggers in repo_service, scan_service, bandit_scanner, semgrep_scanner
- Test suite: 19 passing tests (scan API 200/400, scan service clone error and successful scan, scan persistence complete/failed records, GET /scan/{id} success/404/failed/pending, BanditScanner success/empty/invalid JSON/missing exe/confidence mapping, SemgrepScanner success/empty/invalid JSON/missing exe)
- Test infrastructure: in-memory SQLite with StaticPool, db_session fixture, get_db dependency override
- Dockerfile (python:3.11-slim, copies backend/ and scanners/, exposes port 8000)
- docker-compose.yml (single api service, port 8000, volume mount for dev, PYTHONUNBUFFERED=1)
- Dependencies in requirements.txt (fastapi==0.135.1, uvicorn==0.41.0, bandit==1.9.4, semgrep, pytest==8.3.5, httpx==0.28.1, sqlalchemy==2.0.36)
- README with project description, Docker and local quick start, API endpoint table, curl example, test instructions

---

## Partially Implemented

- Plan doc files: api_design.md has content (scan persistence + GET /scan/{id} design, now fully implemented); finding_schema.md and scanner_architecture.md are empty

---

## Not Implemented Yet

- Frontend (all frontend directories are empty placeholders)
- AI agent layer (agents/ directory is empty)
- Authentication / authorization
- Async scan processing / job queue

---

## Defined Architecture

- 5-layer architecture (Frontend → API → Services → Scanners → AI Agents)
- Scanner plugin system via BaseScanner ABC
- Scanner registry for dynamic scanner discovery
- Separation of concerns: API layer has no business logic, services orchestrate, scanners produce findings
- Database layer isolated in backend/db/ — Base separated from engine/session to prevent circular imports

---

## Existing Documentation

docs/
- architecture.md — 5-layer architecture overview, data flow, logging section, implemented vs planned components
- roadmap.md — 5-phase development plan
- development_workflow.md — three-agent workflow guide with tools, AI roles, session procedures
- COWORK_PROJECT_INSTRUCTIONS.md — Cowork project instructions (loaded into Cowork settings)
- plans/ — api_design.md (scan persistence and GET /scan/{id} design, now implemented), finding_schema.md and scanner_architecture.md (empty)
- adr/ — 001-use-fastapi.md, 002-finding-schema.md, 003-scanner-plugin-interface.md (all written with full content)
- backlog.md — tracked housekeeping items (Pydantic ConfigDict migration, dev dependency split)
- prompts/ — session-start-prompt.md, cowork-summary-prompt.md, desktop-claude-summary-prompt.md, vscode-claude-summary-prompt.md (all with content)
- summaries/ — cowork-summary.md (updated 2026-03-30), desktop-claude-summary.md (updated 2026-03-30), vscode-claude-summary.md (updated 2026-03-31)
- README.md — project description, quick start guides, API endpoints, test instructions

---

## Key Data Model

- Finding (Pydantic): id, title, description, severity (enum), file, line, scanner, confidence
- ScanRequest: repository_url (str)
- ScanResponse: scan_id (str), findings (List[Finding])
- ScanDetailResponse: scan_id (str), repository_url (str), status (str), findings (List[Finding]), created_at (datetime)
- ScanRecord (SQLAlchemy): id (UUID str), repository_url, status (pending/complete/failed), findings (JSON), created_at (DateTime, UTC)

---

## Current System Capability

- POST /scan with a repository URL creates a pending ScanRecord, clones the repo, runs Bandit and Semgrep, parses results into normalized Finding objects, updates the record to complete with serialized findings, cleans up the temp directory, and returns scan_id and findings as JSON
- GET /scan/{id} retrieves a scan by ID, deserializes findings back into Finding objects, returns full scan details including repository_url, status, findings, and created_at. Returns 404 for unknown IDs. Pending and failed scans return findings as empty list.
- Failed scans (clone error or unexpected exception) are persisted with status="failed" before the error response is returned
- Clone failures return 400 with structured error detail; unexpected errors return 500
- GET /health returns a status check
- Logging captures clone operations, scanner execution, finding counts, errors with stack traces, and temp dir cleanup
- 19 unit tests validate the scan API, scan service, scan persistence, GET /scan/{id}, BanditScanner, and SemgrepScanner
- Docker build and run verified — container serves the API on port 8000

---

## Next Logical Steps

1. Begin Phase 3 — AI Analysis Layer design (create design doc in docs/plans/)
2. Address backlog items (Pydantic ConfigDict migration, dev dependency split)
3. Write content for empty plan files (finding_schema.md, scanner_architecture.md)
4. Update docs/architecture.md to reflect GET /scan/{id} as implemented

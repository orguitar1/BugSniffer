BugSniffer — Project State

Last Updated: 2026-03-18
Phase: Phase 2 – Scanner Integration

---

## Backend

Framework: FastAPI (Python)
Status: Core scan pipeline implemented and functional with error handling and tests

---

## Frontend

Framework: React / Next.js (planned)
Status: Not implemented

---

## Implemented Components

- FastAPI application entry point with GET /health endpoint
- POST /scan endpoint accepting repository URL, returning findings
- Structured error handling in scan endpoint: RepoCloneError returns 400, generic exceptions return 500
- Finding Pydantic model with SeverityLevel enum (low/medium/high/critical)
- ScanRequest and ScanResponse models
- Repository cloning service via subprocess (git clone to temp dir)
- RepoCloneError custom exception with temp dir cleanup on failure
- Scan orchestration service with try/finally temp dir cleanup
- BaseScanner ABC with abstract scan() method
- BanditScanner: runs bandit -r via subprocess, parses JSON output, maps Bandit confidence levels (LOW/MEDIUM/HIGH), logs errors
- Scanner registry pattern (get_scanners() returns list of active scanners)
- Test suite: 4 passing tests (scan API 200/400 responses, scan service clone error and successful scan)
- Dependencies pinned in requirements.txt (fastapi==0.135.1, uvicorn==0.41.0, bandit==1.9.4, pytest==8.3.5, httpx==0.28.1)

---

## Partially Implemented

- ADR and plan doc files exist but are empty
- README.md is empty

---

## Not Implemented Yet

- Frontend (all frontend directories are empty placeholders)
- AI agent layer (agents/ directory is empty)
- Database / scan persistence (scans are stateless request-response)
- GET /scan/{id} endpoint
- Authentication / authorization
- Docker setup (docker-compose.yml is empty, no Dockerfile)
- Async scan processing / job queue
- Additional scanners beyond Bandit

---

## Defined Architecture

- 5-layer architecture (Frontend → API → Services → Scanners → AI Agents)
- Scanner plugin system via BaseScanner ABC
- Scanner registry for dynamic scanner discovery
- Separation of concerns: API layer has no business logic, services orchestrate, scanners produce findings

---

## Existing Documentation

docs/
- architecture.md — 5-layer architecture overview and data flow
- roadmap.md — 5-phase development plan
- development_workflow.md — workflow guide with tools, AI roles, session procedures
- plans/ — api_design.md, finding_schema.md, scanner_architecture.md (all empty)
- adr/ — 001-use-fastapi.md, 002-finding-schema.md, 003-scanner-plugin-interface.md (all empty)

---

## Key Data Model

- Finding (Pydantic): id, title, description, severity (enum), file, line, scanner, confidence
- ScanRequest: repository_url (str)
- ScanResponse: findings (List[Finding])

---

## Current System Capability

- POST /scan with a repository URL clones the repo, runs Bandit against it, parses results into normalized Finding objects, cleans up the temp directory, and returns the findings as JSON
- Clone failures return 400 with structured error detail; unexpected errors return 500
- GET /health returns a status check
- 4 unit tests validate the scan API and scan service

---

## Next Logical Steps

1. Add logging across services (repo_service, scan_service)
2. Add GET /scan/{id} endpoint with scan persistence
3. Write content for empty ADR and plan files
4. Add additional scanners beyond Bandit
5. Implement Docker setup
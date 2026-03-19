BugSniffer — Project State

Last Updated: 2026-03-19
Phase: Phase 2 – Scanner Integration

---

## Backend

Framework: FastAPI (Python)
Status: Core scan pipeline implemented with two scanners, logging, error handling, and tests

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
- BanditScanner: runs bandit -r via subprocess, parses JSON output, maps Bandit confidence levels (LOW=0.3, MEDIUM=0.6, HIGH=0.9), logs errors
- SemgrepScanner: runs semgrep --config auto via subprocess, parses JSON output, maps severity (ERROR=high/0.9, WARNING=medium/0.6, INFO=low/0.3), logs errors
- Scanner registry pattern (get_scanners() returns [BanditScanner, SemgrepScanner])
- Logging: root logger configured in main.py (INFO level), module-level loggers in repo_service, scan_service, bandit_scanner, semgrep_scanner
- Test suite: 4 passing tests (scan API 200/400 responses, scan service clone error and successful scan)
- Dependencies in requirements.txt (fastapi==0.135.1, uvicorn==0.41.0, bandit==1.9.4, semgrep, pytest==8.3.5, httpx==0.28.1)

---

## Partially Implemented

- Plan doc files exist but are empty (api_design.md, finding_schema.md, scanner_architecture.md)
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

---

## Defined Architecture

- 5-layer architecture (Frontend → API → Services → Scanners → AI Agents)
- Scanner plugin system via BaseScanner ABC
- Scanner registry for dynamic scanner discovery
- Separation of concerns: API layer has no business logic, services orchestrate, scanners produce findings

---

## Existing Documentation

docs/
- architecture.md — 5-layer architecture overview, data flow, logging section, implemented vs planned components
- roadmap.md — 5-phase development plan
- development_workflow.md — workflow guide with tools, AI roles, session procedures
- plans/ — api_design.md, finding_schema.md, scanner_architecture.md (all empty)
- adr/ — 001-use-fastapi.md, 002-finding-schema.md, 003-scanner-plugin-interface.md (all written with full content)

---

## Key Data Model

- Finding (Pydantic): id, title, description, severity (enum), file, line, scanner, confidence
- ScanRequest: repository_url (str)
- ScanResponse: findings (List[Finding])

---

## Current System Capability

- POST /scan with a repository URL clones the repo, runs Bandit and Semgrep against it, parses results into normalized Finding objects, cleans up the temp directory, and returns the findings as JSON
- Clone failures return 400 with structured error detail; unexpected errors return 500
- GET /health returns a status check
- Logging captures clone operations, scanner execution, finding counts, errors with stack traces, and temp dir cleanup
- 4 unit tests validate the scan API and scan service

---

## Next Logical Steps

1. Add GET /scan/{id} endpoint with scan persistence
2. Write content for empty plan files
3. Implement Docker setup
4. Add tests for SemgrepScanner
5. Write README content

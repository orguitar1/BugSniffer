BugSniffer — Project State

Last Updated: 2026-03-18
Phase: Phase 2 – Scanner Integration

---

## Backend

Framework: FastAPI (Python)
Status: Core scan pipeline implemented and functional

---

## Frontend

Framework: React / Next.js (planned)
Status: Not implemented

---

## Implemented Components

- FastAPI application entry point with GET /health endpoint
- POST /scan endpoint accepting repository URL, returning findings
- Finding Pydantic model with SeverityLevel enum (low/medium/high/critical)
- ScanRequest and ScanResponse models
- Repository cloning service via subprocess (git clone to temp dir)
- RepoCloneError custom exception with temp dir cleanup on failure
- Scan orchestration service with try/finally temp dir cleanup
- BaseScanner ABC with abstract scan() method
- BanditScanner: runs bandit -r via subprocess, parses JSON output to Finding objects
- Scanner registry pattern (get_scanners() returns list of active scanners)
- Dependencies pinned in requirements.txt (fastapi==0.135.1, uvicorn==0.41.0, bandit==1.9.4)

---

## Partially Implemented

- RepoCloneError is raised but not converted to a structured HTTP error response (clients get raw 500)
- BanditScanner silently swallows all exceptions (bare except Exception: pass)
- Finding confidence hardcoded to 0.9 instead of mapping from Bandit's own confidence levels
- ADR and plan doc files exist but are empty
- PROJECT_MAP.md is current; PROJECT_STATE.md was outdated until this update

---

## Not Implemented Yet

- Tests (tests/ directory is empty, no pytest setup)
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
- GET /health returns a status check

---

## Next Logical Steps

1. Write tests for API endpoints, models, and services
2. Convert RepoCloneError to structured HTTP error response
3. Improve BanditScanner error handling (log instead of silently swallowing)
4. Map Bandit confidence levels to Finding confidence field
5. Add GET /scan/{id} endpoint with scan persistence
6. Write content for empty ADR and plan files
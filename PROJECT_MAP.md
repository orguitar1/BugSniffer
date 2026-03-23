# BugSniffer — Project Map

Last verified: 2026-03-23

---

## Project Structure

```
BugSniffer/
├── .env.example                  # Empty — no env vars documented yet
├── .gitignore                    # Ignores .env, __pycache__/, node_modules/, *.pyc, .vscode/, bugsniffer.db
├── Dockerfile                    # python:3.11-slim, copies backend/ and scanners/, exposes port 8000, runs uvicorn
├── PROJECT_MAP.md                # This file — working context map for the project
├── PROJECT_STATE.md              # Current project state snapshot (last updated 2026-03-20)
├── README.md                     # Empty
├── docker-compose.yml            # Single api service, port 8000, volume mount for dev, PYTHONUNBUFFERED=1
├── requirements.txt              # fastapi==0.135.1, uvicorn==0.41.0, bandit==1.9.4, semgrep, pytest==8.3.5, httpx==0.28.1, sqlalchemy==2.0.36
│
├── backend/
│   ├── main.py                   # FastAPI app entry point — configures root logger, calls init_db(), mounts scan router, exposes GET /health
│   ├── api/
│   │   └── routes/
│   │       └── scan.py           # POST /scan endpoint — injects db session via Depends, passes to service, handles RepoCloneError (400) and generic errors (500)
│   ├── db/
│   │   ├── __init__.py           # Empty — makes backend/db a Python package
│   │   ├── base.py               # Base(DeclarativeBase) — SQLAlchemy declarative base, isolated to prevent circular imports
│   │   ├── session.py            # engine, SessionLocal, get_db() — SQLite connection, session factory, FastAPI dependency
│   │   └── init_db.py            # init_db() — creates all tables via Base.metadata.create_all (idempotent)
│   ├── models/
│   │   ├── finding.py            # Finding Pydantic model with SeverityLevel enum (low/medium/high/critical)
│   │   ├── scan.py               # ScanRequest (repository_url) and ScanResponse (scan_id, List[Finding]) models
│   │   └── scan_record.py        # ScanRecord SQLAlchemy ORM model — scan_records table (id, repository_url, status, findings JSON, created_at)
│   └── services/
│       ├── repo_service.py       # clone_repository() — git clones to temp dir, raises RepoCloneError on failure, logs clone operations
│       └── scan_service.py       # scan_repository(url, db) — orchestrates clone, scanner execution, temp dir cleanup, persists ScanRecord, returns ScanResponse
│
├── scanners/
│   ├── base_scanner.py           # BaseScanner ABC — defines abstract scan(repo_path) -> List[Finding]
│   ├── bandit_scanner.py         # BanditScanner — runs bandit -r via subprocess, parses JSON into Findings, maps confidence levels, logs errors
│   ├── semgrep_scanner.py        # SemgrepScanner — runs semgrep --config auto via subprocess, parses JSON into Findings, maps severity levels, logs errors
│   └── registry.py               # get_scanners() — returns list of active scanner instances [BanditScanner, SemgrepScanner]
│
├── agents/                       # Empty (.gitkeep only)
├── frontend/
│   ├── components/               # Empty (.gitkeep only)
│   ├── pages/                    # Empty (.gitkeep only)
│   ├── services/                 # Empty (.gitkeep only)
│   └── styles/                   # Empty (.gitkeep only)
├── prompts/                      # Empty (.gitkeep only)
├── scripts/                      # Empty (.gitkeep only)
├── tests/
│   ├── conftest.py               # pytest fixtures — in-memory SQLite db_session, TestClient with get_db override
│   ├── test_scan_api.py          # Tests for POST /scan (200 with scan_id, 400 clone failure)
│   ├── test_scan_service.py      # Tests for scan_repository (clone error, successful scan returning ScanResponse)
│   ├── test_scan_persistence.py  # Tests for scan persistence (complete record on success, failed record on clone error)
│   └── test_semgrep_scanner.py   # Tests for SemgrepScanner (success, empty stdout, invalid JSON, missing executable)
│
└── docs/
    ├── architecture.md           # 5-layer architecture overview, data flow, logging section, implemented vs planned components
    ├── backlog.md                # Tracked housekeeping items (Pydantic ConfigDict migration, dev dependency split)
    ├── roadmap.md                # 5-phase development plan (foundation through system expansion)
    ├── development_workflow.md   # Workflow guide — tools, AI roles, session procedures, testing
    ├── adr/
    │   ├── 001-use-fastapi.md    # ADR: Use FastAPI as the backend framework
    │   ├── 002-finding-schema.md # ADR: Use a single normalized Finding schema across all scanners
    │   └── 003-scanner-plugin-interface.md  # ADR: Use an ABC and registry for scanner discovery
    └── plans/
        ├── api_design.md         # Design for scan persistence and GET /scan/{id} endpoint
        ├── finding_schema.md     # Empty
        └── scanner_architecture.md  # Empty
```

---

## Implemented Features

- **FastAPI application** with health check (`GET /health`) and scan endpoint (`POST /scan`)
- **Full scan pipeline**: receive URL -> clone repo -> run scanners -> return findings -> cleanup temp dir
- **Finding data model**: Pydantic model with id, title, description, severity (enum), file, line, scanner, confidence
- **Request/response models**: ScanRequest (repository_url) and ScanResponse (scan_id, List[Finding])
- **Scan persistence**: SQLite via SQLAlchemy, ScanRecord table (id UUID, repository_url, status, findings JSON, created_at), database initialized at app startup
- **Database layer**: engine, session factory, get_db() FastAPI dependency, declarative base isolated to prevent circular imports
- **Repository cloning service**: clones via subprocess, creates temp dir, raises RepoCloneError on failure with cleanup
- **Scan orchestration service**: creates pending ScanRecord, runs scanners, updates to complete/failed, commits, returns ScanResponse
- **Scanner plugin interface**: BaseScanner ABC with abstract `scan()` method and `name` attribute
- **Bandit scanner**: runs `bandit -r <path> -f json`, parses JSON output, maps results to Finding objects
- **Semgrep scanner**: runs `semgrep --config auto <path> --json --quiet`, parses JSON output, maps severity and confidence to Finding objects
- **Scanner registry**: centralized `get_scanners()` function returning [BanditScanner, SemgrepScanner]
- **Logging**: root logger configured in main.py (INFO level), module-level loggers in repo_service, scan_service, bandit_scanner, semgrep_scanner
- **API error handling**: RepoCloneError returns 400, generic exceptions return 500 with structured JSON responses
- **Tests**: 10 passing tests covering scan API (200/400), scan service (clone failure, successful scan), scan persistence (complete record, failed record), and SemgrepScanner (success, empty stdout, invalid JSON, missing executable)
- **Docker setup**: Dockerfile (python:3.11-slim) and docker-compose.yml (single api service, port 8000, dev volume mount)

---

## Partially Implemented

- **Documentation**: architecture.md, roadmap.md, and development_workflow.md have content; ADR files have full content; api_design.md has content; finding_schema.md and scanner_architecture.md are still empty
- **README** — file is empty

---

## Not Implemented Yet

- **Frontend** — all frontend directories are empty placeholders
- **AI agent layer** — agents/ directory is empty, no LLM integration
- **Prompt templates** — prompts/ directory is empty
- **GET /scan/{id} endpoint** — designed in docs/plans/api_design.md, not built
- **Authentication / authorization**
- **Async scan processing / job queue** — scans block the HTTP request

# BugSniffer — Project Map

Last verified: 2026-03-30

---

## Project Structure

```
BugSniffer/
├── .env.example                  # Empty — no env vars documented yet
├── .gitignore                    # Ignores .env, __pycache__/, node_modules/, *.pyc, .vscode/, bugsniffer.db
├── .vscode/
│   └── settings.json             # VS Code Python environment settings (tracked in repo, 132 bytes)
├── Dockerfile                    # python:3.11-slim, copies backend/ and scanners/, exposes port 8000, runs uvicorn
├── PROJECT_MAP.md                # This file — structural map of the repository
├── PROJECT_STATE.md              # Current project state snapshot (last updated 2026-03-30)
├── README.md                     # Empty
├── docker-compose.yml            # Single api service, port 8000, volume mount for dev, PYTHONUNBUFFERED=1
├── requirements.txt              # fastapi==0.135.1, uvicorn==0.41.0, bandit==1.9.4, semgrep, pytest==8.3.5, httpx==0.28.1, sqlalchemy==2.0.36
│
├── backend/
│   ├── main.py                   # FastAPI app entry point — configures root logger (INFO), calls init_db(), mounts scan router, exposes GET /health
│   ├── api/
│   │   ├── .gitkeep              # Placeholder
│   │   └── routes/
│   │       └── scan.py           # POST /scan endpoint — injects db session via Depends(get_db), delegates to scan_repository(), handles RepoCloneError (400) and generic errors (500)
│   ├── db/
│   │   ├── __init__.py           # Empty — makes backend/db a Python package
│   │   ├── base.py               # Base(DeclarativeBase) — SQLAlchemy declarative base, isolated to prevent circular imports
│   │   ├── session.py            # engine (SQLite, check_same_thread=False), SessionLocal factory, get_db() FastAPI dependency generator
│   │   └── init_db.py            # init_db() — creates all tables idempotently via Base.metadata.create_all
│   ├── models/
│   │   ├── .gitkeep              # Placeholder
│   │   ├── finding.py            # Finding Pydantic model with SeverityLevel enum (low/medium/high/critical), fields: id, title, description, severity, file, line, scanner, confidence
│   │   ├── scan.py               # ScanRequest (repository_url str) and ScanResponse (scan_id str, findings List[Finding]) Pydantic models
│   │   └── scan_record.py        # ScanRecord SQLAlchemy ORM model — scan_records table (id UUID primary key, repository_url, status pending/complete/failed, findings JSON, created_at DateTime UTC)
│   └── services/
│       ├── .gitkeep              # Placeholder
│       ├── repo_service.py       # clone_repository(url) — git clones to temp dir via subprocess, returns path; RepoCloneError exception with temp dir cleanup on failure; logs clone operations
│       └── scan_service.py       # scan_repository(url, db) — creates pending ScanRecord, clones repo, runs all scanners from registry, updates status to complete/failed, commits to db, cleans up temp dir via shutil.rmtree, returns ScanResponse
│
├── scanners/
│   ├── .gitkeep                  # Placeholder
│   ├── base_scanner.py           # BaseScanner ABC — defines abstract scan(repo_path) -> List[Finding] and name attribute
│   ├── bandit_scanner.py         # BanditScanner — runs bandit -r <path> -f json via subprocess, parses JSON output, maps Bandit confidence levels (LOW=0.3, MEDIUM=0.6, HIGH=0.9) to Finding objects, logs errors
│   ├── semgrep_scanner.py        # SemgrepScanner — runs semgrep --config auto <path> --json --quiet via subprocess, parses JSON output, maps severity (ERROR=high/0.9, WARNING=medium/0.6, INFO=low/0.3) to Finding objects, logs errors
│   └── registry.py               # get_scanners() — returns list of active scanner instances [BanditScanner(), SemgrepScanner()]
│
├── agents/                       # Empty (.gitkeep only) — planned AI agent layer
├── frontend/
│   ├── components/               # Empty (.gitkeep only)
│   ├── pages/                    # Empty (.gitkeep only)
│   ├── services/                 # Empty (.gitkeep only)
│   └── styles/                   # Empty (.gitkeep only)
├── prompts/                      # Empty (.gitkeep only) — planned AI prompt templates
├── scripts/                      # Empty (.gitkeep only)
│
├── tests/
│   ├── .gitkeep                  # Placeholder
│   ├── conftest.py               # pytest fixtures — in-memory SQLite with StaticPool, db_session fixture, get_db dependency override, TestClient factory
│   ├── test_scan_api.py          # 2 tests — valid repo POST /scan returns 200 with scan_id and findings; invalid repo returns 400 with error detail
│   ├── test_scan_service.py      # 2 tests — scan_repository handles clone error gracefully; successful scan returns ScanResponse with findings
│   ├── test_scan_persistence.py  # 2 tests — successful scan writes ScanRecord with status=complete and findings; failed scan writes ScanRecord with status=failed
│   └── test_semgrep_scanner.py   # 4 tests — successful scan returns Finding objects; empty stdout returns []; invalid JSON returns []; missing executable returns []
│
└── docs/
    ├── .gitkeep                  # Placeholder
    ├── architecture.md           # 5-layer architecture overview (Frontend, API, Services, Scanners, AI Agents), data flow, logging section, implemented vs planned components, future considerations
    ├── backlog.md                # 2 tracked housekeeping items: Pydantic ConfigDict migration, dev dependency split
    ├── roadmap.md                # 5-phase development plan: Foundation → Scanner Integration → AI Analysis → Frontend → System Expansion
    ├── development_workflow.md   # Three-agent workflow guide — tools, AI roles (Cowork/Desktop/VS Code), session start/planning/implementation/end procedures, testing strategy, git workflow
    ├── COWORK_PROJECT_INSTRUCTIONS.md  # Full Cowork project instructions — loaded into Claude Cowork project settings
    ├── adr/
    │   ├── 001-use-fastapi.md    # ADR: Use FastAPI as the backend framework — rationale, alternatives considered
    │   ├── 002-finding-schema.md # ADR: Use a single normalized Finding schema across all scanners — field definitions, severity enum
    │   └── 003-scanner-plugin-interface.md  # ADR: Use ABC and registry pattern for scanner plugin discovery — BaseScanner interface, get_scanners() registry
    ├── plans/
    │   ├── api_design.md         # Design doc: scan persistence via SQLite/SQLAlchemy + GET /scan/{id} endpoint — response shapes, persistence model, status transitions, out of scope items
    │   ├── finding_schema.md     # Empty
    │   └── scanner_architecture.md  # Empty
    ├── prompts/
    │   ├── session-start-prompt.md         # Template: paste into all agents at session start to read context files and confirm readiness
    │   ├── cowork-summary-prompt.md        # Template: summary prompt for Claude Cowork
    │   ├── desktop-claude-summary-prompt.md # Template: summary prompt for Desktop Claude Code
    │   └── vscode-claude-summary-prompt.md  # Template: summary prompt for VS Code Claude Code (this session's prompt)
    └── summaries/
        ├── cowork-summary.md       # Cowork session summary — last updated 2026-03-30, records workflow setup, FUSE issue, next steps
        ├── desktop-claude-summary.md # Desktop Claude Code summary — last updated 2026-03-30
        └── vscode-claude-summary.md  # VS Code Claude Code summary — last updated 2026-03-30
```

---

## Implemented Features

- **FastAPI application** with health check (`GET /health`) and scan endpoint (`POST /scan`)
- **Full scan pipeline**: receive URL → clone repo → run scanners → normalize findings → persist results → cleanup temp dir → return response
- **Finding data model**: Pydantic model with id, title, description, severity (enum), file, line, scanner, confidence
- **Request/response models**: ScanRequest (repository_url) and ScanResponse (scan_id, List[Finding])
- **Scan persistence**: SQLite via SQLAlchemy 2.x, ScanRecord table (id UUID, repository_url, status, findings JSON, created_at), database initialized at app startup
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

- **Documentation plans**: api_design.md has full content (scan persistence + GET /scan/{id} design); finding_schema.md and scanner_architecture.md exist but are empty
- **README** — file exists but is empty
- **Environment config** — .env.example exists but is empty

---

## Not Implemented Yet

- **Frontend** — all frontend directories are empty placeholders, no React/Next.js code
- **AI agent layer** — agents/ directory is empty, no LLM integration
- **Prompt templates for AI agents** — prompts/ directory is empty
- **GET /scan/{id} endpoint** — designed in docs/plans/api_design.md, not built
- **Authentication / authorization** — not designed or implemented
- **Async scan processing / job queue** — scans currently block the HTTP request
- **BanditScanner tests** — SemgrepScanner has 4 dedicated tests but BanditScanner has none
- **Scripts** — scripts/ directory is empty

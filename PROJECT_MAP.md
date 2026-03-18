# BugSniffer — Project Map

Last verified: 2026-03-18

---

## Project Structure

```
BugSniffer/
├── .env.example                  # Empty — no env vars documented yet
├── .gitignore                    # Ignores .env, __pycache__/, node_modules/, *.pyc, .vscode/
├── PROJECT_MAP.md                # This file — working context map for the project
├── PROJECT_STATE.md              # Current project state snapshot (last updated 2026-03-18)
├── README.md                     # Empty
├── docker-compose.yml            # Empty
├── requirements.txt              # fastapi==0.135.1, uvicorn==0.41.0, bandit==1.9.4, pytest==8.3.5, httpx==0.28.1
│
├── backend/
│   ├── main.py                   # FastAPI app entry point — mounts scan router, exposes GET /health
│   ├── api/
│   │   └── routes/
│   │       └── scan.py           # POST /scan endpoint — accepts ScanRequest, returns ScanResponse, handles RepoCloneError (400) and generic errors (500)
│   ├── models/
│   │   ├── finding.py            # Finding Pydantic model with SeverityLevel enum (low/medium/high/critical)
│   │   └── scan.py               # ScanRequest (repository_url) and ScanResponse (List[Finding]) models
│   └── services/
│       ├── repo_service.py       # clone_repository() — git clones to temp dir, raises RepoCloneError on failure
│       └── scan_service.py       # scan_repository() — orchestrates clone, scanner execution, and temp dir cleanup
│
├── scanners/
│   ├── base_scanner.py           # BaseScanner ABC — defines abstract scan(repo_path) -> List[Finding]
│   ├── bandit_scanner.py         # BanditScanner — runs bandit -r via subprocess, parses JSON into Findings, maps confidence levels, logs errors
│   └── registry.py               # get_scanners() — returns list of active scanner instances [BanditScanner]
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
│   ├── conftest.py               # pytest fixtures — FastAPI TestClient
│   ├── test_scan_api.py          # Tests for POST /scan (200 success, 400 clone failure)
│   └── test_scan_service.py      # Tests for scan_repository (clone error, successful scan)
│
└── docs/
    ├── architecture.md           # 5-layer architecture overview and data flow description
    ├── roadmap.md                # 5-phase development plan (foundation through system expansion)
    ├── development_workflow.md   # Workflow guide — tools, AI roles, session procedures, testing
    ├── adr/
    │   ├── 001-use-fastapi.md    # Empty
    │   ├── 002-finding-schema.md # Empty
    │   └── 003-scanner-plugin-interface.md  # Empty
    └── plans/
        ├── api_design.md         # Empty
        ├── finding_schema.md     # Empty
        └── scanner_architecture.md  # Empty
```

---

## Implemented Features

- **FastAPI application** with health check (`GET /health`) and scan endpoint (`POST /scan`)
- **Full scan pipeline**: receive URL -> clone repo -> run scanners -> return findings -> cleanup temp dir
- **Finding data model**: Pydantic model with id, title, description, severity (enum), file, line, scanner, confidence
- **Request/response models**: ScanRequest (repository_url) and ScanResponse (List[Finding])
- **Repository cloning service**: clones via subprocess, creates temp dir, raises RepoCloneError on failure with cleanup
- **Scan orchestration service**: iterates scanners from registry, collects findings, always cleans up temp dir via try/finally
- **Scanner plugin interface**: BaseScanner ABC with abstract `scan()` method and `name` attribute
- **Bandit scanner**: runs `bandit -r <path> -f json`, parses JSON output, maps results to Finding objects
- **Scanner registry**: centralized `get_scanners()` function for dynamic scanner discovery
- **API error handling**: RepoCloneError returns 400, generic exceptions return 500 with structured JSON responses
- **Tests**: 4 passing tests covering scan API endpoint (200/400 responses) and scan service (clone failure, successful scan)

---

## Partially Implemented

- **Documentation**: architecture.md, roadmap.md, and development_workflow.md have content, but all ADR files and plan files are empty

---

## Not Implemented Yet

- **Frontend** — all frontend directories are empty placeholders
- **AI agent layer** — agents/ directory is empty, no LLM integration
- **Prompt templates** — prompts/ directory is empty
- **Scan persistence / database** — scans are stateless request-response, no storage
- **GET /scan/{id} endpoint** — mentioned in architecture.md but not built
- **Authentication / authorization**
- **Docker setup** — docker-compose.yml is empty, no Dockerfile
- **Async scan processing / job queue** — scans block the HTTP request
- **Additional scanners** — only Bandit exists
- **README** — file is empty

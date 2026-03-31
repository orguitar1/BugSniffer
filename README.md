# BugSniffer

BugSniffer is an AI-assisted cybersecurity tool that analyzes code repositories for security vulnerabilities. It clones a target repo, runs static analysis scanners (Bandit, Semgrep), normalizes findings into a unified schema with severity and confidence scores, and persists results to a database. Built with Python, FastAPI, SQLAlchemy (SQLite), Bandit, and Semgrep.

**Status:** Phase 2 (Scanner Integration) complete. Phase 3 (AI Analysis Layer) is next. See [docs/roadmap.md](docs/roadmap.md) for the full development plan.

## Quick Start (Docker)

```bash
docker-compose up --build
```

API at http://localhost:8000.

## Quick Start (Local)

Requires Python 3.11+ and both `bandit` and `semgrep` installed locally.

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/scan` | Submit a repository URL for scanning, returns `scan_id` and findings |
| GET | `/scan/{id}` | Retrieve scan results by ID |

Example:

```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"repository_url": "https://github.com/example/repo"}'
```

## Running Tests

```bash
pytest tests/ -v
```

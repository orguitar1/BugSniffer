# ShopSniffer — Agent Instructions

Every agent reads this file at the start of every session.

---

## What This Project Is

ShopSniffer is a multi-tenant SaaS Shopify app that monitors store health and provides an AI assistant. The full product vision is in `docs/plans/product-vision-draft.md`. The technical architecture is in `docs/architecture.md`.

## Tech Stack

- Python 3.11+, FastAPI
- PostgreSQL via SQLAlchemy 2.x, Alembic for migrations
- arq + Redis for async jobs
- React / Next.js frontend (embedded Shopify app via App Bridge)
- Lighthouse via headless Chrome for performance scanning
- LLM API for AI conversation (provider TBD)
- Docker / docker-compose

## Layer Architecture

Six layers, dependencies flow downward only:

1. **API Layer** (`backend/api/`) — HTTP endpoints, Shopify auth, webhooks. No business logic.
2. **Services Layer** (`backend/services/`) — Business logic, orchestration. AI Services live here as specialized services, not a separate layer.
3. **Scanner Layer** (`scanners/`) — Health detection. Produces typed results (ScanSuccess / ScanFailure).
4. **Data Layer** (`backend/db/`, `backend/models/`) — Persistence, tenant isolation. ORM models use `*_record.py` naming.
5. **Integrations Layer** (`backend/integrations/`) — External service clients (Shopify, LLM, Redis). All rate-limited with timeouts.

## Hard Architectural Rules

These are non-negotiable. They apply to every module, every PR, every session.

1. **Scanner results must be a discriminated type.** `ScanSuccess` or `ScanFailure`. Never a bare list where empty means both "clean" and "crashed."
2. **No silent exception swallowing in any detection or analysis path.** Errors propagate or are recorded with explicit status metadata. A `try/except` that returns a default value without recording the failure is a bug.
3. **Database operations that create-then-update must handle failure at each boundary.** If the initial record creation fails, the update path must not assume the record exists.
4. **All external API calls must have explicit timeout, retry, and circuit-breaker behavior defined at the client level.** No integration call should be able to hang indefinitely.

## Three-Agent Workflow

- **Claude Cowork** — Orchestrator. Architecture decisions, planning, code review (read-only). Writes only `docs/summaries/cowork-summary.md`.
- **Claude Code (Desktop)** — Independent reviewer. Code quality review, summary validation. Writes only `docs/summaries/desktop-claude-summary.md`.
- **Claude Code (VS Code)** — Implementation engineer. The only agent that writes code. Maintains `PROJECT_STATE.md`, `PROJECT_MAP.md`, `docs/summaries/vscode-claude-summary.md`.

Full workflow details: `docs/development_workflow.md`

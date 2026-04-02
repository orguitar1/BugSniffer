# ShopSniffer — Project State

Last Updated: [to be filled after first implementation session]
Phase: Pre-implementation — architecture and workflow documents in place, no code written yet.

---

## Backend

Framework: FastAPI (Python 3.11+)
Database: PostgreSQL via SQLAlchemy 2.x + Alembic
Async Jobs: arq + Redis
Status: Not yet implemented

---

## Frontend

Framework: React / Next.js (embedded Shopify app via App Bridge)
Status: Not yet implemented

---

## Implemented Components

None yet. The project is in the documentation and architecture phase.

---

## Partially Implemented

None.

---

## Not Implemented Yet

- Full backend (API layer, services, scanners, integrations, data models)
- Full frontend
- AI agent layer
- Shopify OAuth and app installation flow
- Database schema and migrations
- Async job system
- Docker setup

---

## Defined Architecture

See `docs/architecture.md` for the full architecture plan.

- 6-layer architecture (API → Services → Scanners → Data → Integrations, with AI Services inside Services)
- Scanner plugin system via BaseScanner ABC with typed results (ScanSuccess/ScanFailure)
- Scanner registry for dynamic scanner discovery
- Multi-tenant data model with tenant isolation at the query level
- arq + Redis for async background jobs
- Integrations layer for all external service clients (Shopify, LLM, Redis)

---

## Existing Documentation

- CLAUDE.md — hard rules, tech stack, layer names (every agent reads this)
- docs/architecture.md — full architecture plan (6 layers, phase boundaries, repo structure)
- docs/development_workflow.md — three-agent workflow, session procedures, engineering principles
- docs/COWORK_PROJECT_INSTRUCTIONS.md — Cowork project instructions
- docs/plans/product-vision-draft.md — product brief (source of truth, 18 sections)
- docs/plans/design-phase-notes.md — deferred technical questions (10 sections)
- docs/prompts/ — 9 agent prompt templates
- docs/summaries/ — 3 agent summary files (bootstrap entries)

---

## Next Logical Steps

1. Scaffold project structure (directories, requirements.txt, Docker setup, .gitignore, .env.example)
2. Set up PostgreSQL connection, SQLAlchemy base, Alembic migrations
3. Create FastAPI entry point with health endpoint and first passing test

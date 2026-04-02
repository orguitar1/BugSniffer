# ShopSniffer — Architecture Plan

Status: Reviewed by all three agents — final draft.
Date: 2026-04-02

This document defines the technical architecture for ShopSniffer. It is the primary reference for all implementation work. Every design decision should trace back to the product brief (`docs/plans/product-vision-draft.md`). Detailed component designs (scanner specs, AI pipeline, data schemas) will live in separate documents under `docs/plans/` — this document defines the system shape.

---

## 1. System Overview

ShopSniffer is a multi-tenant SaaS application that runs as a Shopify app. It installs via the Shopify App Store, authenticates via OAuth, maintains persistent access to each merchant's store, runs periodic and on-demand health scans, and provides a conversational AI assistant that can explain findings, answer questions, and edit theme code.

The core loop: **Install → Scan → Findings → AI Conversation → Optional Code Fix**.

The system talks to three categories of external services: Shopify APIs (store data, themes, app permissions), headless Chrome/Lighthouse (performance scanning), and LLM providers (AI conversation and analysis). Each has different latency, reliability, and cost characteristics. The architecture treats all three as external integrations behind explicit client abstractions.

### Tech Stack

- **Backend:** Python 3.11+, FastAPI
- **Database:** PostgreSQL via SQLAlchemy 2.x, Alembic for schema migrations
- **Async Jobs:** arq + Redis
- **Frontend:** React / Next.js (embedded Shopify app via App Bridge)
- **Performance Scanning:** Lighthouse via headless Chrome
- **AI:** LLM API calls (provider TBD during AI layer design)
- **Containerization:** Docker / docker-compose

---

## 2. Layer Architecture

The system is organized into six layers. Dependencies flow downward — upper layers call lower layers, never the reverse.

```
┌─────────────────────────────────────┐
│            API Layer                │  ← HTTP endpoints, Shopify auth, webhooks
├─────────────────────────────────────┤
│          Services Layer             │  ← Business logic, orchestration
│  ┌───────────────────────────────┐  │
│  │    AI Services (specialized)  │  │  ← Analysis, verification, confidence
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│          Scanner Layer              │  ← Health detection (performance, SEO, security)
├─────────────────────────────────────┤
│          Data Layer                 │  ← Models, persistence, tenant isolation
├─────────────────────────────────────┤
│       Integrations Layer            │  ← Shopify client, LLM client, job queue
└─────────────────────────────────────┘
```

### API Layer

Handles HTTP requests, Shopify OAuth flow, session token validation, webhook handlers (including mandatory GDPR webhooks), and response formatting. Contains no business logic.

Location: `backend/api/`

### Services Layer

Contains all business logic and orchestration. Scan orchestration, conversation management, theme operations, notification dispatch, interaction record creation. Services call the Scanner Layer, Data Layer, and Integrations Layer.

**AI Services** live within the Services Layer as specialized services, not as a separate peer layer. The AI pipeline (analysis agent → verification agent → confidence calibration) is orchestrated by a conversation service that coordinates LLM calls (via the Integrations Layer) with scan data (via the Data Layer). The AI services do not call the Scanner Layer directly — if verification requires fresh scan data, the conversation service requests it through the scan orchestration service, maintaining a clean dependency direction.

Location: `backend/services/`

### Scanner Layer

Executes health detection. Each scanner type implements a common interface and produces typed results. Scanners are registered via a registry pattern (carried forward from BugSniffer's scanner plugin system).

Scanners do not interpret their findings — they detect and report. Interpretation is the AI services' job.

Phase 1 scanners: Performance (Lighthouse), basic SEO checks.
Future scanners: Security/permissions audit, third-party app impact analysis.

Location: `scanners/`

### Data Layer

SQLAlchemy ORM models, Pydantic request/response models, database session management, query utilities. All data is tenant-scoped — every query filters by merchant. The declarative base is isolated in its own module to prevent circular imports (pattern carried forward from BugSniffer). Schema migrations are managed via Alembic — `create_all()` is not used in production.

All models (ORM and Pydantic) live in `backend/models/` with a naming convention: `*_record.py` for SQLAlchemy ORM models, all other files are Pydantic models. This avoids the confusion of having two separate `models/` directories at different depths.

Location: `backend/db/` (session, base, migrations) and `backend/models/` (all models)

### Integrations Layer

Client abstractions for all external services. Each client handles authentication, rate limiting, retries, timeouts, and circuit-breaking for its service. This layer exists so that the rest of the application never makes raw HTTP calls or deals with external service quirks directly.

Clients: Shopify API client (REST + GraphQL, rate-limit aware, API version tracked), LLM client (model routing, token tracking, fallback handling), Redis client (shared by job queue and caching).

Location: `backend/integrations/`

---

## 3. Shopify App Requirements

These are non-negotiable constraints imposed by the Shopify platform. They affect the API layer design from day one and are gate checks for App Store approval.

- **Session token authentication** via Shopify App Bridge. The app runs as an embedded app inside Shopify admin. Auth is not traditional OAuth session cookies — it uses short-lived session tokens verified on each request.
- **Mandatory GDPR webhooks:** `customers/redact`, `shop/redact`, `customers/data_request`. The data model must support efficient lookup and deletion by merchant and by customer.
- **App lifecycle webhooks:** `app/uninstalled` is how the system knows a merchant removed the app — triggers data cleanup and subscription cancellation. Distinct from the GDPR `shop/redact` webhook, which handles data deletion requests.
- **API versioning:** Shopify deprecates API versions quarterly. The Shopify client must track which version it targets and the system must have a process for version migration.
- **Rate limits:** REST API: 2 calls/second per app per store. GraphQL: 50 cost points/second. The Shopify client must enforce these with queuing, not just retry-on-429.
- **App review requirements:** HTTPS everywhere, embedded app standards, proper error handling for revoked access tokens, webhook delivery verification.
- **Theme limit:** Shopify stores have a ~20 theme limit. The theme management service must track themes it creates and clean up unpublished preview themes proactively.

---

## 4. Scanner Architecture

Scanners follow an abstract base class with a registry pattern, carried forward from BugSniffer. The key differences from BugSniffer's implementation:

**New interface:** Scanners receive a store context (store URL, API credentials, scan configuration), not a filesystem path.

**Typed results:** Scanner return types distinguish success from failure. A scanner that crashes must never be indistinguishable from a scanner that found no issues.

```python
# Conceptual — exact implementation in detailed design doc
@dataclass
class ScanSuccess:
    findings: list[Finding]

@dataclass
class ScanFailure:
    error: str
    partial_findings: list[Finding]  # any findings collected before failure

ScanResult = ScanSuccess | ScanFailure
```

**Finding model:** Findings include `category` (performance / seo / security / app-impact), `affected_url` or `affected_asset`, `severity`, `actionable` flag (can the AI fix this?), `recommended_action` text, and a reference back to the scan. The exact schema is defined in a separate data model design doc.

**Registry:** `get_scanners()` returns the active scanner set. Scanners can be enabled/disabled per scan type or merchant tier.

Detailed scanner specifications (Lighthouse integration, SEO check rules, security audit scope) will be in `docs/plans/scanner-design.md`.

---

## 5. Data Model Shape

The full schema is a separate design document (`docs/plans/data-model-design.md`). This section defines the core entities and their relationships.

**Merchant** — the tenant. Linked to a Shopify store via shop domain. Holds subscription tier, install date, settings.

**Store** — Shopify store metadata. One merchant may manage multiple stores (agency use case). All data queries are scoped to a store.

**Scan** — a single scan execution. References a store, has a type (performance / seo / security / full), status (pending / running / complete / failed), timestamps, and a link to the job that executed it.

**Finding** — a single detected issue. References a scan. Categorized, severity-rated, with actionable flag and recommended action.

**Conversation** — an AI chat session. References a store. Contains message history, linked scans, linked theme operations.

**ThemeOperation** — a record of AI code editing. References a conversation. Tracks: source theme, preview theme ID, changes made (structured), plain-language description, merchant decision (previewing / published / rolled-back / abandoned), timestamps.

**InteractionRecord** — the unified timeline entry. Links conversations, scans, theme operations, and escalations into a single per-store chronological view. This is what the support team sees.

**Subscription** — tracks a merchant's current tier, usage counts (scans, AI interactions), billing cycle, and cap enforcement. Linked to Merchant. Usage-based limits are enforced via this entity.

**Tenant isolation rule:** Every query that touches merchant data must filter by store. No query path should be able to return data across stores. This is enforced at the query utility level in the Data Layer, not left to individual service methods.

---

## 6. Async Job System

Scans, theme operations, and post-publish health checks are background jobs. They cannot block HTTP requests.

**Queue:** arq with Redis. Lightweight, asyncio-native (pairs with FastAPI), sufficient for the project's current scale. If the project outgrows arq, migrating to Celery is straightforward — job definitions are async functions either way.

**Job types:**

- Scheduled scan — runs on a timer per store (frequency depends on tier)
- On-demand scan — triggered by merchant or AI conversation
- Post-publish health check — triggered automatically after a theme is published
- Theme operation — duplicate theme, apply changes, cleanup abandoned previews

**Job lifecycle:** Every job creates or updates a database record with status transitions (pending → running → complete/failed). Job failures are recorded with error details, never silently swallowed.

**Retry policy:** Retry behavior is defined per job type, not globally. Transient failures (e.g., Lighthouse timeout) are worth retrying once with backoff. Non-idempotent operations (e.g., theme edits mid-progress) must not auto-retry. Details in each job's implementation.

**Dead letter handling:** After max retries, a permanently failed job is surfaced — not silently dropped. Failed scans are visible to the merchant with a clear status. Failed theme operations are flagged for support review.

**Concurrency:** Redis-backed rate limiting ensures Shopify API rate limits are respected even when multiple jobs run concurrently for different stores. Headless Chrome instances are pooled with a configurable maximum.

---

## 7. AI System Overview

The AI is a conversational assistant backed by a multi-agent verification pipeline. Full design in `docs/plans/ai-system-design.md`. This section defines how it fits into the architecture.

**Conversation service** (Services Layer) orchestrates all AI interactions. It manages conversation state, decides when to call the LLM, assembles context (scan data + conversation history + store metadata), and routes between the analysis and verification steps.

**AI pipeline:**

1. **Analysis step** — generates the explanation or recommendation from scan data and conversation context. Uses the LLM client from the Integrations Layer.
2. **Verification step** — fact-checks the analysis output against raw scan data. Does the data actually support what was said?
3. **Confidence calibration** — adjusts response language based on data certainty. Ambiguous data produces hedged responses.

**Context management:** Scan results, conversation history, and code context compete for the LLM's context window. The conversation service summarizes older context and keeps recent interactions verbatim. Strategy details in the AI system design doc.

**Fallback:** If the LLM provider is unavailable, the dashboard and scan results remain accessible. The AI chat shows a clear "temporarily unavailable" state. The system never pretends the AI is working when it isn't.

---

## 8. Hard Architectural Rules

These are non-negotiable constraints. They apply to every module, every PR, every session.

1. **Scanner results must be a discriminated type.** `ScanSuccess` or `ScanFailure`. Never a bare list where empty means both "clean" and "crashed."

2. **No silent exception swallowing in any detection or analysis path.** Errors propagate or are recorded with explicit status metadata. A `try/except` that returns a default value without recording the failure is a bug.

3. **Database operations that create-then-update must handle failure at each boundary.** If the initial record creation fails, the update path must not assume the record exists.

4. **All external API calls must have explicit timeout, retry, and circuit-breaker behavior defined at the client level.** No integration call should be able to hang indefinitely. This applies to Shopify API, LLM providers, and any future external service.

These rules derive from the BugSniffer fresh agent audit, which found that silent scanner failures, broad exception swallowing, and missing commit-boundary handling were the three most critical issues in the codebase. ShopSniffer does not repeat these mistakes.

---

## 9. Phase Boundaries

The architecture supports the full product vision from day one, but implementation is phased. Each phase is a shippable state.

### Phase 1 — Scan + Dashboard + Basic AI Chat

- Shopify OAuth app installation flow
- Store registration and merchant data model
- Performance scanning via Lighthouse
- Basic SEO checks
- Findings storage and retrieval
- Merchant dashboard showing scan results and findings
- Basic AI chat: explain findings, answer questions about store health
- Scheduled and on-demand scans
- Mandatory GDPR webhook handlers

Phase 1 validates the core loop: install → scan → see results → ask AI about them.

### Phase 2 — Theme Code Editing

- Theme duplication via Shopify Theme API
- AI code changes in preview themes
- Plain-language changelogs for merchants
- Preview → publish → rollback flow
- Post-publish health check scans
- Theme cleanup for abandoned previews

Phase 2 adds the core differentiator. It depends on Phase 1 being stable.

### Phase 3 — Advanced Analysis + Support

- Security and permissions audit (scope depends on Shopify API access — validate early)
- Third-party app impact analysis (requires app-to-script mapping database)
- Full interaction records and support team tooling
- Human escalation workflow from AI to support
- Notification system (email + Shopify admin)
- Multi-agent AI verification pipeline (analysis → verification → confidence calibration)

### Future

- Multi-store management for agencies
- Internal business analytics dashboard
- Tiered subscription enforcement
- Multilingual AI responses

---

## 10. Repository Structure

The tree below shows the target structure. Files marked with a phase number (e.g., "Phase 2") should be created when implementing that phase, not as empty placeholders during earlier phases.

```
ShopSniffer/
├── CLAUDE.md                        # Hard rules, tech stack, layer names — every agent reads this
├── PROJECT_STATE.md                 # Current project state (maintained by VS Code Claude)
├── PROJECT_MAP.md                   # Repository structure map (maintained by VS Code Claude)
├── README.md                        # Project description, setup instructions
├── requirements.txt                 # Python dependencies (pinned)
├── docker-compose.yml               # PostgreSQL, Redis, API service
├── Dockerfile                       # API service container
├── .env.example                     # Required environment variables documented
├── .gitignore
│
├── alembic/                         # Database schema migrations (Alembic)
│   ├── alembic.ini
│   ├── env.py
│   └── versions/                    # Migration scripts
│
├── backend/
│   ├── main.py                      # FastAPI app entry point
│   ├── api/
│   │   ├── routes/                  # Endpoint handlers (scan, chat, webhook, etc.)
│   │   ├── auth/                    # Shopify OAuth and session token verification
│   │   └── webhooks/                # Shopify webhook handlers (GDPR, app lifecycle)
│   ├── services/
│   │   ├── scan_service.py          # Scan orchestration
│   │   ├── conversation_service.py  # AI chat orchestration
│   │   ├── theme_service.py         # Theme operations (Phase 2)
│   │   ├── notification_service.py  # Alert dispatch (Phase 3)
│   │   └── ai/                      # AI-specific services
│   │       ├── analysis.py          # Analysis step
│   │       ├── verification.py      # Verification step
│   │       └── confidence.py        # Confidence calibration
│   ├── models/                      # All models — ORM (*_record.py) and Pydantic (all others)
│   ├── db/
│   │   ├── base.py                  # SQLAlchemy DeclarativeBase (isolated)
│   │   └── session.py               # Engine, session factory, get_db()
│   └── integrations/
│       ├── shopify_client.py        # Shopify REST + GraphQL, rate-limited
│       ├── llm_client.py            # LLM provider abstraction
│       └── redis_client.py          # Shared Redis connection
│
├── scanners/
│   ├── base_scanner.py              # BaseScanner ABC (typed results)
│   ├── registry.py                  # Scanner registry
│   ├── performance_scanner.py       # Lighthouse integration
│   └── seo_scanner.py              # SEO checks
│
├── jobs/
│   ├── worker.py                    # arq worker entry point
│   ├── scan_jobs.py                 # Scan job definitions
│   └── theme_jobs.py               # Theme operation jobs (Phase 2)
│
├── tests/
│   ├── conftest.py                  # Fixtures: in-memory SQLite, TestClient, dependency overrides
│   ├── test_api/
│   ├── test_services/
│   ├── test_scanners/
│   └── test_integrations/
│
└── docs/
    ├── architecture.md              # This document
    ├── development_workflow.md       # Three-agent workflow and session procedures
    ├── COWORK_PROJECT_INSTRUCTIONS.md
    ├── plans/
    │   ├── product-vision-draft.md  # Product brief (source of truth)
    │   ├── design-phase-notes.md    # Deferred technical questions
    │   ├── scanner-design.md        # Detailed scanner specs (future)
    │   ├── data-model-design.md     # Full schema design (future)
    │   └── ai-system-design.md      # AI pipeline design (future)
    ├── adr/                         # Architectural decision records
    ├── prompts/                     # Agent prompt templates (9 files)
    └── summaries/                   # Agent session summaries (3 files)
```

---

## Appendix: Decisions Made During Architecture Design

These decisions were discussed across all three agents before this document was written:

- **Fresh start over incremental migration.** The BugSniffer codebase is a stateless scan pipeline; ShopSniffer is a multi-tenant SaaS product. The gap is structural. Patterns carry forward; code does not.
- **PostgreSQL from day one.** Multi-tenant isolation, concurrent writes from background workers, JSONB columns, GDPR cascade deletes — all PostgreSQL-native concerns. SQLAlchemy abstracts the engine. Test suite uses in-memory SQLite for speed.
- **arq over Celery.** Lighter setup, asyncio-native (pairs with FastAPI), sufficient for current scale. Redis is already needed for caching and rate limiting. Migration to Celery later is straightforward if needed.
- **AI services within Services Layer, not a peer layer.** The AI pipeline is orchestrated by the conversation service. It consumes scan data and LLM client calls but doesn't own independent entry points. Keeping it inside Services maintains a clean dependency direction.
- **"Integrations" not "Infrastructure."** The layer contains external service adapters (Shopify, LLM, Redis), not deployment infrastructure. The name should reflect the contents.
- **Alembic for schema migrations.** BugSniffer used `create_all()` which doesn't support schema evolution. ShopSniffer uses Alembic from day one for repeatable, versioned migrations against PostgreSQL.
- **Flat models directory with naming convention.** All models (ORM and Pydantic) in `backend/models/`. ORM files use `*_record.py` suffix. Avoids two separate `models/` directories causing import confusion.
- **Daily fresh agent audits.** A fresh agent (no prior context) audits the codebase at the start of every session. Findings feed into that session's planning. Problems are caught the day after they're introduced.

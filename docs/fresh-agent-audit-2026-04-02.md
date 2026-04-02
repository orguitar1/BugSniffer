# BugSniffer — Fresh Agent Audit

**Date:** 2026-04-02
**Auditor:** Fresh Claude session (no prior context, no summaries read)
**Scope:** Full codebase review against PROJECT_MAP.md

---

## 1. Architecture Assessment

The module structure is clean and well-organized. Separation between API routes, services, scanners, models, and database layer is clear, with no circular dependencies detected. The layering (API -> Services -> Scanners) follows the intended architecture.

**Finding 1.1**

- **Location:** `backend/services/scan_service.py` + `backend/models/scan.py` + `backend/models/scan_record.py`
- **Issue:** Missing domain layer — Pydantic response models (ScanResponse, ScanDetailResponse) are coupled directly to the service layer, and the service layer directly constructs API response objects. As the system grows (AI agents, async processing), this coupling will make it difficult to introduce new consumers of scan results without importing API-specific models.
- **Severity:** Moderate
- **Recommendation:** Introduce a thin domain layer that decouples persistence models from API response models. Services return domain objects; the API layer transforms them into response schemas.

**Finding 1.2**

- **Location:** `backend/db/init_db.py`
- **Issue:** Magic import pattern — `import backend.models.scan_record  # noqa: F401` exists solely to trigger SQLAlchemy ORM registration. This is implicit and fragile; a new ORM model added without a corresponding import here will silently fail to create its table.
- **Severity:** Moderate
- **Recommendation:** Use an explicit model registry or document this pattern prominently so future developers don't miss it.

**Finding 1.3**

- **Location:** `scanners/registry.py`
- **Issue:** Scanner list is hardcoded with no extensibility mechanism — no config file, no environment variable, no plugin discovery. Adding a scanner requires editing code.
- **Severity:** Minor
- **Recommendation:** Make scanner list configurable via environment variable or config, or add entry-point based discovery.

---

## 2. Code Quality Weak Points

**Finding 2.1 — CRITICAL**

- **Location:** `backend/services/scan_service.py`, line ~30 (broad `except Exception`)
- **Issue:** The entire scan pipeline is wrapped in a single `except Exception` block that catches everything from clone failures to scanner crashes to database errors. The caller receives a generic 500 with no detail about what failed. Scanner errors are indistinguishable from infrastructure errors.
- **Severity:** Critical
- **Recommendation:** Narrow exception handling: catch RepoCloneError separately (already done in route layer), catch scanner errors distinctly, and let unexpected errors propagate with full traceback logging.

**Finding 2.2**

- **Location:** `scanners/bandit_scanner.py` and `scanners/semgrep_scanner.py` — `subprocess.run()` calls
- **Issue:** No timeout set on subprocess execution. A hanging scanner (e.g., Semgrep on a massive monorepo) blocks the HTTP request indefinitely.
- **Severity:** Moderate
- **Recommendation:** Add `timeout=<seconds>` to all `subprocess.run()` calls. Catch `subprocess.TimeoutExpired` and return a meaningful error.

**Finding 2.3**

- **Location:** `scanners/bandit_scanner.py`, line ~30 and `scanners/semgrep_scanner.py` (similar pattern)
- **Issue:** Both scanners catch `except Exception`, log it, and return empty list `[]`. The caller cannot distinguish "scanner found no vulnerabilities" from "scanner crashed." This is a silent failure that directly undermines the tool's core purpose — if a scanner fails, the user gets a clean bill of health instead of an error.
- **Severity:** Critical
- **Recommendation:** Either raise a custom `ScannerExecutionError` or return a Result type that distinguishes "no findings" from "scanner failed."

**Finding 2.4**

- **Location:** `backend/services/scan_service.py`, lines ~35-41 (finally block)
- **Issue:** Cleanup uses `shutil.rmtree(repo_path, ignore_errors=True)`. If cleanup fails, temporary directories accumulate silently with no logging.
- **Severity:** Moderate
- **Recommendation:** Log cleanup failures. Consider a periodic cleanup job for orphaned temp directories.

**Finding 2.5**

- **Location:** `backend/models/finding.py`
- **Issue:** Finding.id is a plain string populated from different sources: Bandit uses `test_id` (e.g., "B101"), Semgrep uses a UUID. No uniqueness guarantee across scanners — if two scanners produce the same ID string for different findings, they collide.
- **Severity:** Moderate
- **Recommendation:** Make Finding.id a compound of (scanner_name, original_id) or always generate a fresh UUID and store the scanner-specific ID in a separate field.

**Finding 2.6**

- **Location:** `backend/models/scan_record.py`
- **Issue:** `findings` column is typed as `Optional[list]` — no type validation on what goes into the JSON blob. Malformed data written here will cause deserialization failures in `get_scan_by_id`.
- **Severity:** Minor
- **Recommendation:** Use `Optional[List[dict]]` type hint and add validation on write.

---

## 3. Test Coverage Gaps

**Finding 3.1**

- **Location:** `tests/test_scan_service.py`
- **Issue:** No test for scanner execution failure. Tests cover RepoCloneError and successful scan, but not: scanner raises exception, scanner returns malformed data, or scanner hangs.
- **Severity:** Moderate
- **Recommendation:** Add tests for: (a) scanner raises `Exception` during scan, (b) scanner returns unexpected data types.

**Finding 3.2**

- **Location:** `tests/test_scan_api.py`
- **Issue:** Only two tests (valid repo 200, invalid repo 400). Missing tests for: malformed JSON body, missing `repository_url` field, database errors during scan creation, generic server errors.
- **Severity:** Moderate
- **Recommendation:** Add negative/edge case tests for the API endpoint.

**Finding 3.3**

- **Location:** `tests/test_bandit_scanner.py` and `tests/test_semgrep_scanner.py`
- **Issue:** No timeout tests. No tests for what happens when subprocess hangs or when the executable produces partial/corrupted output.
- **Severity:** Moderate
- **Recommendation:** Add timeout and partial-output tests once timeout is implemented.

**Finding 3.4**

- **Location:** `tests/` (overall)
- **Issue:** No integration tests. All tests mock subprocess calls and database interactions. There is no test that actually clones a repo and runs a scanner.
- **Severity:** Moderate
- **Recommendation:** Add an optional integration test (marked `pytest.mark.slow`) that exercises the real pipeline against a small test repository.

**Finding 3.5**

- **Location:** `tests/test_get_scan.py`
- **Issue:** No test for corrupted/malformed findings JSON in the database. If someone manually edits the DB or a bug writes bad data, the GET endpoint behavior is untested.
- **Severity:** Minor
- **Recommendation:** Add edge case test for malformed findings deserialization.

---

## 4. Refactoring Opportunities

**Finding 4.1**

- **Location:** `scanners/bandit_scanner.py` and `scanners/semgrep_scanner.py`
- **Issue:** Nearly identical pattern: run subprocess -> parse JSON -> map results -> catch exceptions -> return findings or empty list. The only differences are the command, the JSON path to results, and the field mapping.
- **Severity:** Minor
- **Recommendation:** Extract a common `SubprocessScanner` base class in `base_scanner.py` that handles subprocess execution, JSON parsing, and error handling. Subclasses only provide command construction and result mapping.

**Finding 4.2**

- **Location:** `backend/services/scan_service.py` and `backend/api/routes/scan.py`
- **Issue:** Exception handling for `RepoCloneError` exists in both the service and the route. The service catches it, logs it, writes "failed" to DB, and re-raises; the route catches it again and returns 400. This dual handling creates confusion about which layer owns the error.
- **Severity:** Minor
- **Recommendation:** Decide on one layer for error-to-HTTP-status translation. Either the service raises domain exceptions and the route translates, or use FastAPI exception handlers.

**Finding 4.3**

- **Location:** `backend/models/scan.py`
- **Issue:** `ScanResponse` and `ScanDetailResponse` have overlapping fields (`scan_id`, `findings`). ScanDetailResponse is essentially ScanResponse + metadata.
- **Severity:** Minor
- **Recommendation:** Have `ScanDetailResponse` extend `ScanResponse` to eliminate duplication.

---

## 5. Hidden Bug Risks

**Finding 5.1 — CRITICAL**

- **Location:** `backend/services/scan_service.py`, lines ~17-26
- **Issue:** Race condition in scan creation. The service creates a ScanRecord with status "pending" and commits it (line ~23). If this commit fails (database locked, disk full), the exception is caught by the broad `except Exception`, which tries to update the same record to "failed" — but the record was never committed. The client gets a 500 with no scan_id. Meanwhile, if the commit succeeds but the clone or scan fails, the record exists as "pending" but may never be updated if the update-to-"failed" commit also fails.
- **Severity:** Critical
- **Recommendation:** Use explicit transaction management. Consider returning scan_id to client immediately after successful pending commit, then processing the scan asynchronously (this is noted as "not implemented yet" in the map, and it's a real need, not just a nice-to-have).

**Finding 5.2**

- **Location:** `backend/db/session.py`
- **Issue:** SQLite with `check_same_thread=False` is used. If the application is deployed with multiple Uvicorn workers or any async framework, concurrent writes will cause "database is locked" errors. This is a ticking time bomb for production.
- **Severity:** Moderate
- **Recommendation:** Use PostgreSQL for any non-dev deployment, or add explicit documentation that SQLite is dev-only. Add a startup warning if running with multiple workers.

**Finding 5.3**

- **Location:** `backend/services/scan_service.py`, line ~34
- **Issue:** The `findings` list is serialized to JSON via `[f.model_dump() for f in all_findings]` and stored in the database. But `get_scan_by_id` deserializes by passing dicts back through `Finding(**f)`. If the Finding model schema ever changes (field added/removed/renamed), existing database records will fail to deserialize with no migration path.
- **Severity:** Moderate
- **Recommendation:** Add schema versioning to the findings JSON, or use a migration-aware serialization format. At minimum, add a try/except around Finding deserialization in `get_scan_by_id`.

**Finding 5.4**

- **Location:** `scanners/base_scanner.py`
- **Issue:** `name` is declared as a class attribute type hint but not enforced at runtime. A concrete scanner that forgets to set `name` will raise `AttributeError` only when `name` is accessed during scan execution — not at import or instantiation time.
- **Severity:** Minor
- **Recommendation:** Add `__init_subclass__` validation or an `__init__` check in BaseScanner.

---

## 6. PROJECT_MAP.md Accuracy

Every claim in PROJECT_MAP.md was verified against the actual codebase:

| Claim | Verdict |
|-------|---------|
| .env.example is empty | **Accurate** |
| backend/main.py: logger, init_db, scan router, /health | **Accurate** |
| backend/api/routes/scan.py: POST /scan, GET /scan/{id} | **Accurate** |
| backend/db/base.py: Base(DeclarativeBase) | **Accurate** |
| backend/db/session.py: SQLite engine, SessionLocal, get_db | **Accurate** |
| backend/db/init_db.py: creates all tables | **Accurate** |
| backend/models/finding.py: Pydantic Finding + SeverityLevel enum | **Accurate** |
| backend/models/scan.py: ScanRequest, ScanResponse, ScanDetailResponse | **Accurate** |
| backend/models/scan_record.py: ScanRecord ORM model | **Accurate** |
| backend/services/repo_service.py: clone_repository, RepoCloneError | **Accurate** |
| backend/services/scan_service.py: scan_repository, get_scan_by_id | **Accurate** |
| scanners/base_scanner.py: BaseScanner ABC | **Accurate** |
| scanners/bandit_scanner.py: BanditScanner | **Accurate** |
| scanners/semgrep_scanner.py: SemgrepScanner | **Accurate** |
| scanners/registry.py: get_scanners() returns [BanditScanner(), SemgrepScanner()] | **Accurate** |
| 19 tests across 7 test files | **Accurate** (19 test functions confirmed) |
| docs/plans/finding_schema.md: empty | **Accurate** |
| docs/plans/scanner_architecture.md: empty | **Accurate** |
| All frontend/, agents/, prompts/, scripts/ directories: empty (.gitkeep only) | **Accurate** |

**PROJECT_MAP.md is accurate and complete. No phantom entries, no missing files.**

---

## Findings Summary

### Critical (3)

1. **Broad exception handling hides scan failures** — `scan_service.py` catches all exceptions uniformly, making it impossible to distinguish clone errors, scanner crashes, and infrastructure failures.
2. **Scanner failures return empty findings** — Both scanners catch exceptions and return `[]`, making a crashed scanner indistinguishable from a clean scan. This directly undermines the tool's core purpose.
3. **Race condition in scan record creation** — Database commit failure during "pending" record creation leads to inconsistent state with no recovery path.

### Moderate (10)

1. No subprocess timeout on scanner execution
2. Silent temp directory cleanup failures
3. Finding ID collision risk across scanners
4. SQLite not production-safe with concurrent access
5. Missing domain layer (Pydantic/ORM coupling)
6. Magic import pattern for ORM registration
7. No tests for scanner execution failures
8. Sparse API endpoint test coverage
9. No integration tests
10. No schema versioning for serialized findings

### Minor (6)

1. Scanner registry not configurable
2. Code duplication across scanner implementations
3. Overlapping response model fields
4. BaseScanner.name not enforced at instantiation
5. Untyped findings column in ORM model
6. No test for corrupted findings deserialization

---

## Overall Assessment

The BugSniffer codebase has a **solid architectural foundation** — clean module boundaries, no circular dependencies, good separation between API/services/scanners, and an accurate project map. For an early-stage project, the structure is well-thought-out and will support growth.

However, the codebase has **serious error handling deficiencies** that must be addressed before any real-world use. The combination of broad exception catching, silent scanner failures, and race conditions in scan creation means the system can silently produce incorrect results (clean scan reports when scanners actually crashed) and lose scan requests without any indication to the user or operator.

**The single biggest risk:** Scanner failures returning empty findings lists. A security scanning tool that silently reports "no vulnerabilities found" when its scanners crash is worse than having no tool at all — it creates false confidence. This must be fixed before anything else.

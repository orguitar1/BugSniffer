# ShopSniffer Development Workflow

This document defines how the ShopSniffer project is developed and maintained.

The goal is to ensure development remains organized, resumable, and architecturally consistent.


## 1. Development Tools

Editor: Visual Studio Code
Architecture, Planning & Orchestration: Claude Cowork
Code Review & Summary Validation: Claude Code (Desktop App)
Implementation & Code Changes: Claude Code (VS Code Extension)
Version Control: GitHub
Backend Framework: FastAPI
Database: PostgreSQL (Alembic migrations)
Async Jobs: arq + Redis
Containerization: Docker / docker-compose


## 2. AI Agent Roles

ShopSniffer uses three AI agents with strictly defined responsibilities.


### Claude Cowork — Orchestrator & Context Keeper

Responsibilities:
- System architecture decisions
- Feature planning and prioritization
- Shopify integration and scanner architecture design
- AI agent pipeline design
- Reviewing code (read-only — never writes or modifies code)
- Orchestrating development sessions
- Deciding the next development steps
- Generating implementation prompts for VS Code Claude Code
- Maintaining cowork-summary.md

File Access: Read-only during sessions. Writes only to docs/summaries/cowork-summary.md at session end.


### Claude Code (Desktop App) — Independent Reviewer

Responsibilities:
- Reviewing code changes for quality and correctness
- Validating that summaries accurately reflect what was built
- Cross-checking the work of VS Code Claude Code
- Providing feedback during the planning phase
- Maintaining desktop-claude-summary.md

File Access: Read-only during sessions. Writes only to docs/summaries/desktop-claude-summary.md at session end.


### Claude Code (VS Code Extension) — Implementation Engineer

Responsibilities:
- Writing and modifying all code
- Creating new files and modules
- Debugging and refactoring
- Running tests
- Reviewing its own changes before committing
- Generating implementation summaries
- Maintaining vscode-claude-summary.md, PROJECT_STATE.md, and PROJECT_MAP.md

File Access: Full read-write access to the entire repository.


## 3. Shared Context Files

All three agents read these files at the start of every session to establish shared context.

- docs/summaries/cowork-summary.md — Maintained by Claude Cowork
- docs/summaries/desktop-claude-summary.md — Maintained by Claude Code (Desktop)
- docs/summaries/vscode-claude-summary.md — Maintained by Claude Code (VS Code)
- PROJECT_STATE.md — Maintained by Claude Code (VS Code)
- PROJECT_MAP.md — Maintained by Claude Code (VS Code)


## 4. Session Workflow

### Daily Fresh Agent Audit (Before Session Start)

Before starting each development session, run a fresh agent audit:

1. Open a completely new agent session with no prior ShopSniffer context.
2. Give the agent the codebase and PROJECT_MAP.md only — no summaries, no conversation history.
3. The agent independently evaluates: architecture, code quality, test coverage, hidden risks.
4. Collect the audit findings.

This runs every session, not periodically. Problems are caught the day after they're introduced, not after multiple sessions of code have been built on top of them. The audit prompt is in `docs/prompts/fresh-agent-audit-prompt.md`.


### Session Start

1. User shares fresh audit findings (if any) with all three agents.
2. User opens a new conversation with each agent.
3. User asks all three agents to read the shared context files.
4. All agents pick up context from the same source of truth.
5. If the audit found issues, they go to the top of the planning queue before any new work.


### Planning Phase

1. User and Claude Cowork discuss the current project state and decide the next 2–3 development steps — simple, clear, and effective.
2. User shares the proposed steps with Desktop Claude Code and VS Code Claude Code for feedback.
3. All three agents discuss and agree on the plan.
4. Before generating implementation prompts, Claude Cowork leads a failure-first review of each step:
   - What assumptions are we making? Are any of them fragile?
   - What are the most likely failure modes?
   - What edge cases could surface during implementation?
   - Are there dependencies between steps that could cascade if one fails?
   This step is especially important before features that introduce new integration points (Shopify APIs, LLM calls, async jobs, new data stores).
5. Claude Cowork provides tailored implementation prompts for VS Code Claude Code. The prompts should reflect any failure modes or edge cases identified in step 4.


### Implementation Phase (Repeat for Each Step)

1. VS Code Claude Code implements the step.
2. After implementation, all three agents review the changes using structured checklists:

   Claude Cowork (Architectural Review — read-only):
   - Does the implementation match the design document?
   - Are there any deviations from agreed architecture or data flow?
   - Do new modules, endpoints, or models fit the existing separation of concerns?
   - Were the failure modes identified in planning actually handled?
   - Are there any new architectural assumptions that weren't discussed?

   Desktop Claude Code (Code Quality Review — read-only):
   - Are there concrete bugs, logic errors, or unhandled exceptions?
   - Are edge cases covered (empty inputs, None values, error states)?
   - Is the code consistent with existing patterns and style conventions?
   - Are tests meaningful — do they test behavior, not just happy paths?
   - Are there any security concerns, dependency issues, or deprecation risks?

   VS Code Claude Code (Implementation Defense):
   - Explain any trade-offs or deviations from the design.
   - Identify anything left intentionally unhandled and justify why.
   - Confirm all new code paths have test coverage.
   - Flag any technical debt introduced and whether it belongs on the backlog.

3. Reviewers must raise specific, concrete issues — not general "looks good" approvals. If no issues are found, each reviewer states what they checked and why they're confident.
4. Once all agents are satisfied, user commits the changes.
5. Move to the next step.


### Session End

1. VS Code Claude Code updates:
   - PROJECT_STATE.md
   - PROJECT_MAP.md
   - docs/summaries/vscode-claude-summary.md
   - Verifies all updates are accurate.
2. Desktop Claude Code reads VS Code Claude Code's summary, reviews the changes, and updates:
   - docs/summaries/desktop-claude-summary.md
3. Claude Cowork reads both summaries, checks the codebase directly, and updates:
   - docs/summaries/cowork-summary.md
   - Flags any discrepancies between the three summaries.
4. Commit all summary and state file updates.
5. Push everything to GitHub (development commits + summary commits all go up together).

This triple-summary approach ensures no single agent's perspective becomes the unchecked source of truth.


## 5. Design-First Development

Complex features should be designed before implementation.

Design documents are stored in docs/plans/ and define:

- Module responsibilities
- File structure
- Data models
- Request flow
- Edge cases

Implementation begins only after the design is reviewed and agreed upon by all three agents.


## 6. Testing Strategy

All features must be tested before committing.

Automated Tests: Written using pytest, stored in tests/.
Test Database: In-memory SQLite with StaticPool for fast unit tests. The application targets PostgreSQL — test utilities should avoid SQLite-specific behavior.
Mocking: External services (Shopify API, LLM providers) are mocked in tests. No test should make real external API calls.
Tenant Isolation: Tests must verify that data queries are properly scoped to the correct store/merchant.

ShopSniffer has more complex testing needs than BugSniffer: mocking Shopify API responses, testing webhook signature verification, testing async job execution, and verifying tenant isolation. These are addressed incrementally as each subsystem is built.


## 7. Git Workflow

Commit after each completed step during a session. Push all commits at the end of the session.

Avoid using git add . — always add specific files to reduce the risk of committing sensitive files.


## 8. Project Memory Structure

ShopSniffer maintains three independent sources of project memory.

Source Code: GitHub repository.
Architecture & Design History: docs/, docs/plans/, docs/adr/.
Project State & Continuity: PROJECT_STATE.md, PROJECT_MAP.md, and docs/summaries/.

This guarantees the project can always be resumed from any point.


## 9. Engineering Principles

- Modular architecture
- Separation of concerns (API → requests, services → logic, scanners → detection, AI → reasoning)
- Design-first development
- Failure-first planning — identify what can go wrong before writing code
- Documented architectural decisions
- Incremental feature development
- Structured review with concrete checklists — no vague approvals
- Daily fresh audits at the start of every session
- Hard architectural rules enforced always (see CLAUDE.md)


## 10. Lessons from BugSniffer

ShopSniffer is a successor project to BugSniffer, a code security scanner built with the same three-agent workflow. Several process lessons carried forward:

- **Design-first saved us from rework.** Every feature that had a design doc before implementation went smoother than those that didn't. This is now a hard rule for complex features.
- **The fresh agent audit caught real bugs.** BugSniffer's audit found 3 critical issues (silent scanner failures, broad exception swallowing, race conditions in record creation) that the regular agents had normalized. Daily audits prevent this.
- **The stress-test process improved the product brief significantly.** Running an adversarial review prompt against the product brief surfaced 8 concrete gaps that were fixed before any code was written. Design documents should be stress-tested before implementation begins.
- **Silent failures are the worst kind of bug in a detection tool.** A security/health scanner that reports "clean" when its scanners actually crashed creates false confidence. The discriminated ScanResult type exists because of this lesson.
- **Structured reviews beat "looks good."** Requiring reviewers to state what they checked and why they're confident produces better outcomes than asking "any issues?"

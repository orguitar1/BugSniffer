BugSniffer Development Workflow


This document defines how the BugSniffer project is developed and maintained.

The goal is to ensure development remains organized, resumable, and architecturally consistent.


1. Development Tools

Editor: Visual Studio Code
Architecture, Planning & Orchestration: Claude Cowork
Code Review & Summary Validation: Claude Code (Desktop App)
Implementation & Code Changes: Claude Code (VS Code Extension)
Version Control: GitHub
Backend Framework: FastAPI


2. AI Agent Roles

BugSniffer uses three AI agents with strictly defined responsibilities.


Claude Cowork — Orchestrator & Context Keeper

Responsibilities:
- System architecture decisions
- Feature planning and prioritization
- API and scanner architecture design
- AI agent pipeline design
- Reviewing code (read-only — never writes or modifies code)
- Orchestrating development sessions
- Deciding the next development steps
- Generating implementation prompts for VS Code Claude Code
- Maintaining cowork-summary.md

File Access: Read-only during sessions. Writes only to docs/summaries/cowork-summary.md at session end.


Claude Code (Desktop App) — Independent Reviewer

Responsibilities:
- Reviewing code changes for quality and correctness
- Validating that summaries accurately reflect what was built
- Cross-checking the work of VS Code Claude Code
- Providing feedback during the planning phase
- Maintaining desktop-claude-summary.md

File Access: Read-only during sessions. Writes only to docs/summaries/desktop-claude-summary.md at session end.


Claude Code (VS Code Extension) — Implementation Engineer

Responsibilities:
- Writing and modifying all code
- Creating new files and modules
- Debugging and refactoring
- Running tests
- Reviewing its own changes before committing
- Generating implementation summaries
- Maintaining vscode-claude-summary.md, PROJECT_STATE.md, and PROJECT_MAP.md

File Access: Full read-write access to the entire repository.


3. Shared Context Files

All three agents read these files at the start of every session to establish shared context.

docs/summaries/cowork-summary.md — Maintained by Claude Cowork
docs/summaries/desktop-claude-summary.md — Maintained by Claude Code (Desktop)
docs/summaries/vscode-claude-summary.md — Maintained by Claude Code (VS Code)
PROJECT_STATE.md — Maintained by Claude Code (VS Code)
PROJECT_MAP.md — Maintained by Claude Code (VS Code)


4. Session Workflow

SESSION START (Every Monday, or sooner if context degrades)

1. User opens a new conversation with each agent.
2. User asks all three agents to read the shared context files.
3. All agents pick up context from the same source of truth.

PLANNING PHASE

1. User and Claude Cowork discuss the current project state and decide the next 3 development steps — simple, clear, and effective.
2. User shares the proposed steps with Desktop Claude Code and VS Code Claude Code for feedback.
3. All three agents discuss and agree on the plan.
4. Claude Cowork provides tailored implementation prompts for VS Code Claude Code.

IMPLEMENTATION PHASE (Repeat for Each Step)

1. VS Code Claude Code implements the step.
2. After implementation, all three agents review the changes:
   - Claude Cowork reviews architecture and correctness (read-only).
   - Desktop Claude Code reviews code quality (read-only).
   - VS Code Claude Code reviews its own changes.
3. Once all agents are satisfied, user commits the changes.
4. Move to the next step.

SESSION END

1. Push all commits to GitHub.
2. VS Code Claude Code updates:
   - PROJECT_STATE.md
   - PROJECT_MAP.md
   - docs/summaries/vscode-claude-summary.md
   - Verifies all updates are accurate.
3. Desktop Claude Code reads VS Code Claude Code's summary, reviews the changes, and updates:
   - docs/summaries/desktop-claude-summary.md
4. Claude Cowork reads both summaries, checks the codebase directly, and updates:
   - docs/summaries/cowork-summary.md
   - Flags any discrepancies between the three summaries.

This triple-summary approach ensures no single agent's perspective becomes the unchecked source of truth.


5. Design-First Development

Complex features should be designed before implementation.

Design documents are stored in docs/plans/ and define:

- Module responsibilities
- File structure
- Data models
- Request flow
- Edge cases

Implementation begins only after the design is reviewed and agreed upon by all three agents.


6. Testing Strategy

All features must be tested locally before committing.

Manual API Testing: Endpoints tested using curl or Postman.
Automated Tests: Written using pytest, stored in tests/.

Early tests focus on verifying that API endpoints respond correctly and services execute without errors.


7. Git Workflow

Commit after each completed step during a session. Push all commits at the end of the session.

Avoid using git add . — always add specific files to reduce the risk of committing sensitive files.


8. Project Memory Structure

BugSniffer maintains three independent sources of project memory.

Source Code: GitHub repository.
Architecture & Design History: docs/, docs/plans/, docs/adr/.
Project State & Continuity: PROJECT_STATE.md, PROJECT_MAP.md, and docs/summaries/.

This guarantees the project can always be resumed from any point.


9. Engineering Principles

- Modular architecture
- Separation of concerns
- Design-first development
- Documented architectural decisions
- Incremental feature development
- Triple-agent review before commits

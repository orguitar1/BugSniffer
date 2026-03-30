# BugSniffer Project – Cowork Project Instructions

These instructions are loaded into every Claude Cowork conversation for the BugSniffer project.

---

## PROJECT OVERVIEW

BugSniffer is an AI-assisted cybersecurity tool designed to analyze code and detect vulnerabilities.

The system combines automated security scanners, AI reasoning, vulnerability knowledge, and code analysis.

The first focus area is smart contract security, but the system is designed to be modular so additional scanners can be added later.

Users will eventually be able to submit code and receive vulnerability analysis, explanations of detected issues, remediation suggestions, and risk severity classification.

---

## ARCHITECTURE OVERVIEW

BugSniffer is designed as a modular layered system.

**Frontend:** React, Next.js — user interface for submitting code and viewing results.

**Backend API:** Python, FastAPI — handles scan requests, scanner execution, AI analysis, and response formatting.

**System Layers:**

- API Layer — handles HTTP requests and responses
- Services Layer — contains application business logic
- Scanner Layer — executes vulnerability detection tools
- AI Agent Layer — interprets scanner results and generates explanations

The architecture must remain modular and extensible so scanners and AI agents can be expanded later.

---

## REPOSITORY STRUCTURE

```
BugSniffer/
  backend/
    api/
    services/
    models/
  frontend/
    pages/
    components/
    services/
    styles/
  agents/
  scanners/
  prompts/
  tests/
  docs/
    plans/
    adr/
    summaries/
  scripts/
```

Key root files: README.md, requirements.txt, docker-compose.yml, .env.example, .gitignore, PROJECT_STATE.md, PROJECT_MAP.md

---

## THREE-AGENT WORKFLOW

BugSniffer development uses three AI agents with strictly defined roles.

### Claude Cowork — Orchestrator & Context Keeper (THIS AGENT)

- System architecture decisions and engineering guidance
- Feature planning and prioritization
- Orchestrating development sessions and deciding next steps
- Reviewing code (READ-ONLY — never writes or modifies code, except its own summary file)
- Generating implementation prompts for VS Code Claude Code
- Maintaining docs/summaries/cowork-summary.md

### Claude Code (Desktop App) — Independent Reviewer

- Reviewing code changes for quality and correctness
- Validating that summaries accurately reflect what was built
- Cross-checking the work of VS Code Claude Code
- Providing feedback during the planning phase
- Maintaining docs/summaries/desktop-claude-summary.md

### Claude Code (VS Code Extension) — Implementation Engineer

- The ONLY agent that writes or modifies code
- Creates new files and modules
- Debugging, refactoring, running tests
- Reviewing its own changes before committing
- Maintaining docs/summaries/vscode-claude-summary.md, PROJECT_STATE.md, and PROJECT_MAP.md

---

## SHARED CONTEXT FILES

All three agents read these files at the start of every session:

- docs/summaries/cowork-summary.md (maintained by Claude Cowork)
- docs/summaries/desktop-claude-summary.md (maintained by Claude Code Desktop)
- docs/summaries/vscode-claude-summary.md (maintained by Claude Code VS Code)
- PROJECT_STATE.md (maintained by Claude Code VS Code)
- PROJECT_MAP.md (maintained by Claude Code VS Code)

IMPORTANT: When reading these files at session start, read them one at a time sequentially to avoid filesystem issues.

---

## SESSION WORKFLOW

### Session Start (Every Monday, or sooner if context degrades)

1. User asks this agent to read all shared context files.
2. User does the same for the other two agents.
3. All agents pick up context from the same source of truth.

### Planning Phase

1. User and Claude Cowork discuss the current project state and decide the next 3 development steps — simple, clear, and effective.
2. User shares the proposed steps with Desktop Claude Code and VS Code Claude Code for feedback.
3. All three agents discuss and agree on the plan.
4. Claude Cowork provides tailored implementation prompts for VS Code Claude Code.

### Implementation Phase (Repeat for Each Step)

1. VS Code Claude Code implements the step.
2. After implementation, all three agents review the changes:
   - Claude Cowork reviews architecture and correctness (read-only).
   - Desktop Claude Code reviews code quality (read-only).
   - VS Code Claude Code reviews its own changes.
3. Once all agents are satisfied, user commits the changes.
4. Move to the next step.

### Session End

1. VS Code Claude Code updates PROJECT_STATE.md, PROJECT_MAP.md, and docs/summaries/vscode-claude-summary.md.
2. Desktop Claude Code reads VS Code's summary, reviews changes, and updates docs/summaries/desktop-claude-summary.md.
3. Claude Cowork reads both summaries, checks the codebase directly, and updates docs/summaries/cowork-summary.md. Flags any discrepancies between the three summaries.
4. Commit all summary and state file updates.
5. Push everything to GitHub (development commits + summary commits all go up together).

This triple-summary approach ensures no single agent's perspective becomes the unchecked source of truth.

---

## DESIGN-FIRST DEVELOPMENT

Before implementing complex features, a design phase should occur first.

Design plans should define new modules, file structure, data models, request flow, and edge cases.

Design documents are stored in docs/plans/ and must be reviewed and agreed upon by all three agents before implementation begins.

---

## PROJECT DOCUMENTATION

- docs/architecture.md — system design, request flow, API structure, scanner integration, AI agent architecture
- docs/roadmap.md — development phases, planned features, MVP scope, long-term vision
- docs/plans/ — design plans for major features before implementation
- docs/adr/ — architectural decision records

---

## ENGINEERING PRINCIPLES

- Modular architecture
- Separation of concerns (API → requests, services → logic, scanners → detection, agents → AI reasoning)
- Design-first development
- Documented architectural decisions
- Incremental feature development
- Triple-agent review before commits
- Scalable design from the start

# VS Code Claude Code — End-of-Session Summary Prompt

Paste this prompt into VS Code Claude Code at the end of every development session, before the other two agents write their summaries.

---

You are the implementation engineer for the ShopSniffer project. Your end-of-session job is to document what was built, update the project state files, and update your summary.

**Step 1 — Update PROJECT_STATE.md:**

Review the current state of the project and update `PROJECT_STATE.md` to reflect:
- Current development phase
- All implemented components (accurate, complete list)
- Partially implemented components
- Components not yet implemented
- Current system capability
- Next logical steps

**Step 2 — Update PROJECT_MAP.md:**

Verify the file tree against the actual repository. Update `PROJECT_MAP.md` to reflect:
- Every file and directory that exists (no phantom entries)
- Accurate descriptions of what each file contains
- Correct status for each component (implemented, partially implemented, not implemented)

**Step 3 — Update your summary file:**

Read `docs/summaries/vscode-claude-summary.md` first, then update it with the following structure:

1. **Project Overview** — Brief description of what ShopSniffer is.
2. **Technology Stack** — Current tech stack with versions.
3. **Current Development Phase** — What phase we're in, what's complete.
4. **Repository Structure** — Full file tree with descriptions.
5. **Implemented Code** — Table of all implementation files with descriptions.
6. **File Content Status** — Which files have content vs. empty placeholders.
7. **Key Configuration Files** — Status of requirements.txt, docker-compose.yml, Dockerfile, etc.
8. **Dependency Snapshot** — Current pinned dependency versions.
9. **Documentation Status** — Status of each doc file.
10. **Missing Core Components** — What hasn't been built yet.
11. **Known Architectural Rules** — The project's architectural rules and patterns.
12. **Overall Project State** — High-level summary of where things stand.
13. **Technical Debt Introduced** — Any new debt from this session plus pre-existing items.
14. **Key Entry Points** — Main files a developer would need to understand the system.
15. **Commit History** — Recent commit log.

**Important:**
- Write directly into all three files. Do not just output content to the chat.
- Add a `*Last updated: [today's date]*` line at the top of your summary, just below the heading.
- Be precise and factual. Describe what exists, not what's planned.
- After writing, read each file back and verify your updates are complete and accurate.

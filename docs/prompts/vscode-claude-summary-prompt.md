# VS Code Claude Code — End-of-Session Summary Prompt

Paste this prompt into VS Code Claude Code at the end of every development session.

---

Analyze the current BugSniffer repository and update the file `docs/summaries/vscode-claude-summary.md` with a structured summary of the project.

This file is read by all three agents (Cowork, Desktop Claude Code, and you) at the start of every session to establish shared context. It must be accurate, current, and reflect the actual state of the codebase.

Read the file first, then update it following this exact structure:

1. **Project Overview** — One short paragraph describing what the project is and its purpose.

2. **Technology Stack** — Quick snapshot of technologies used or planned. Example format:
   - Backend Framework: FastAPI (Python)
   - Frontend Framework: React / Next.js (planned, not implemented)
   - Testing: pytest with httpx
   - Containers: Docker / docker-compose
   - AI Integration: LLM-based analysis agents (planned)

3. **Current Development Phase** — Which phase the project is in. What has been implemented vs what is still missing.

4. **Repository Structure** — Clean tree view of the repository.

5. **Implemented Code** — List files that contain real implementation code and briefly describe what they do. If no implementation code exists yet, explicitly state that.

6. **File Content Status** — Classify files into three categories:
   - Files with meaningful content (with brief descriptions)
   - Files that exist but are empty placeholders
   - Directories containing only .gitkeep

7. **Key Configuration Files** — Summarize the purpose and status of requirements.txt, docker-compose.yml, .env.example, README.md, .gitignore, etc. Indicate whether they contain meaningful configuration or are empty placeholders.

8. **Dependency Snapshot** — List important dependencies declared in the project (Python from requirements.txt, Node from package.json if present). If dependency files exist but are empty, explicitly state that.

9. **Documentation Status** — List documentation files and what they describe. Indicate if any exist but are currently empty.

10. **Missing Core Components** — Identify important parts of the system not yet implemented.

11. **Known Architectural Rules** — Summarize architectural constraints defined in documentation.

12. **Overall Project State** — Short summary of how far along the project is, whether it is mostly documentation or implementation, and what the next logical development steps should be.

13. **Technical Debt Introduced** — List any technical debt flagged during implementation defense this session. For each item, note: what it is, why it was deferred rather than fixed, and whether it was added to `docs/backlog.md`. If no tech debt was introduced, state that explicitly.

14. **Key Entry Points** — Identify important files that act as entry points or central components. If none exist yet, explicitly state that.

15. **Commit History** — Include the full commit log.

**Important:**
- Write the summary directly into `docs/summaries/vscode-claude-summary.md`. Do not output it to the chat.
- Add a `*Last updated: [today's date]*` line at the top, just below the heading.
- Use clear section headings.
- Keep the summary concise but informative.
- After writing, read the file back and verify it is accurate and complete.

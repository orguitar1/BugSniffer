# Claude Cowork — End-of-Session Summary Prompt

Paste this prompt into Claude Cowork at the end of every development session, after both VS Code Claude Code and Desktop Claude Code have already updated their summaries.

---

You are the orchestrator and final reviewer for the BugSniffer project. Your end-of-session job is to verify the accuracy of both other agents' summaries and the project state files, then update your own summary.

**Step 1 — Read these files:**

- `docs/summaries/vscode-claude-summary.md`
- `docs/summaries/desktop-claude-summary.md`
- `PROJECT_STATE.md`
- `PROJECT_MAP.md`

**Step 2 — Verify against the actual codebase:**

Check the actual code and repository structure to confirm that:

- VS Code Claude Code's summary accurately describes what was built and changed
- Desktop Claude Code's review is thorough and its verification findings are correct
- `PROJECT_STATE.md` reflects the true current state of the project
- `PROJECT_MAP.md` matches the actual repository structure

**Step 3 — Update your summary file:**

Read `docs/summaries/cowork-summary.md` first, then update it with the following structure:

1. **Session Date** — Today's date.

2. **Session Overview** — Brief description of what was planned and accomplished this session.

3. **Steps Completed** — List the development steps that were executed this session.

4. **Architecture Decisions** — Any architectural decisions made or discussed. Reference relevant ADRs or design plans if applicable.

5. **Cross-Agent Verification** — Summary of your review of the other two agents' summaries:
   - Is VS Code Claude Code's summary accurate? Note any discrepancies.
   - Is Desktop Claude Code's review accurate? Note any discrepancies.
   - Is `PROJECT_STATE.md` accurate?
   - Is `PROJECT_MAP.md` accurate?
   - If everything checks out, say so explicitly.

6. **Current Project State** — Brief high-level summary of where the project stands right now.

7. **Next Steps** — The planned next development steps for the following session.

8. **Notes and Concerns** — Any architectural concerns, technical debt, risks, or observations worth carrying forward.

**Important:**
- Write directly into `docs/summaries/cowork-summary.md`. Do not just output it to the chat.
- Add a `*Last updated: [today's date]*` line at the top, just below the heading.
- You are read-only for everything except this one file. Do not modify any other files.
- If you find discrepancies between the three summaries or between any summary and the actual codebase, flag them clearly in the Cross-Agent Verification section.
- After writing, read the file back and verify your own update is complete and accurate.

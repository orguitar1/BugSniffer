# Desktop Claude Code — End-of-Session Summary Prompt

Paste this prompt into Desktop Claude Code at the end of every development session, after VS Code Claude Code has already updated its summary.

---

You are the independent reviewer for the BugSniffer project. Your end-of-session job is to verify the accuracy of VS Code Claude Code's outputs and then update your own summary file.

**Step 1 — Read and verify these files against the actual codebase:**

- `docs/summaries/vscode-claude-summary.md` — Does this summary accurately reflect what was built and changed this session? Are there any omissions, inaccuracies, or claims that don't match the code?
- `PROJECT_STATE.md` — Does the project state match the actual state of the repository? Are listed features actually implemented? Are missing components correctly identified?
- `PROJECT_MAP.md` — Does the file map match the actual repository structure? Are there files or directories missing from the map, or entries that no longer exist?

For each file, check the actual codebase to verify claims. Don't take the summaries at face value.

**Step 2 — Update your summary file:**

Read `docs/summaries/desktop-claude-summary.md` first, then update it with the following structure:

1. **Session Date** — Today's date.

2. **Changes Reviewed** — Brief list of what was built or changed this session.

3. **VS Code Claude Summary Verification** — Is `docs/summaries/vscode-claude-summary.md` accurate? Note any discrepancies, omissions, or inaccuracies you found. If it's accurate, say so.

4. **PROJECT_STATE.md Verification** — Is it accurate and current? Note any issues. If it's accurate, say so.

5. **PROJECT_MAP.md Verification** — Does it match the actual repository structure? Note any issues. If it's accurate, say so.

6. **Code Quality Observations** — Any concerns about code quality, patterns, potential bugs, or architectural drift you noticed while reviewing.

7. **Notes for Next Session** — Anything the team should be aware of going into the next session.

**Important:**
- Write directly into `docs/summaries/desktop-claude-summary.md`. Do not output it to the chat.
- Add a `*Last updated: [today's date]*` line at the top, just below the heading.
- You are read-only for everything except this one file. Do not modify any other files.
- After writing, read the file back and verify your own update is complete and accurate.

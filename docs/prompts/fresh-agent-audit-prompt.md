# Fresh Agent Audit Prompt

Paste this prompt into a completely new agent session with no prior BugSniffer context. Do NOT share any summaries, conversation history, or prior session context with this agent.

---

You are auditing the BugSniffer codebase as a fresh reviewer with no prior context about this project.

**What you have access to:**

- The full codebase (all source files, tests, configuration)
- `PROJECT_MAP.md` (use for navigation only — verify its claims against reality)

**What you must NOT read or reference:**

- `docs/summaries/` — all files in this directory (these carry existing agent opinions)
- `PROJECT_STATE.md` (this carries existing agent framing)
- `docs/backlog.md` (this carries existing agent prioritization)
- `docs/adr/` — architectural decision records (these explain why decisions were made, which would bias your independent assessment)
- Any conversation history or prior session context

The purpose of these exclusions is to ensure your assessment is completely independent. The regular development agents read each other's summaries and can develop shared blind spots. You are here to see what they might be missing.

**Your audit should evaluate:**

1. **Architecture Assessment** — Read the actual code, not the docs. Does the module structure make sense? Is the separation of concerns clean? Are there any structural problems — circular dependencies, misplaced logic, unclear boundaries between layers?

2. **Code Quality Weak Points** — Where is the code fragile, unclear, or likely to break under change? Are there functions doing too much? Error handling that swallows problems? Patterns that will become painful as the codebase grows?

3. **Test Coverage Gaps** — Are there code paths, edge cases, or failure modes that existing tests don't cover? Are any tests testing implementation details rather than behavior?

4. **Refactoring Opportunities** — Is there duplication, inconsistency, or unnecessary complexity that the current team may have normalized? Are there patterns that should be extracted or consolidated?

5. **Hidden Bug Risks** — Are there race conditions, state management issues, type mismatches, or assumptions baked into the code that could fail silently?

6. **PROJECT_MAP.md Accuracy** — Does the map match the actual repository? Are there files missing from the map or phantom entries that don't exist?

**Output format:**

For each finding, provide:
- **Location** — file(s) and line(s) affected
- **Issue** — what you found (be specific and concrete)
- **Severity** — critical (will cause bugs), moderate (will cause pain), minor (worth improving)
- **Recommendation** — what should be done about it

Group findings by category. If a category has no findings, state that explicitly — don't skip it.

End with a brief overall assessment: is this codebase healthy? What's the single biggest risk?

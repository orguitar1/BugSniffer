# ShopSniffer — Project Map

Last verified: [to be filled after first implementation session]

---

## Project Structure

The repository currently contains documentation only. The target code structure is defined in `docs/architecture.md` Section 10. This file will be updated with the actual file tree after the first implementation session.

```
ShopSniffer/
├── CLAUDE.md                          # Hard rules, tech stack, layer names — every agent reads this
├── PROJECT_MAP.md                     # This file
├── PROJECT_STATE.md                   # Current project state snapshot
│
└── docs/
    ├── architecture.md                # Architecture plan (6 layers, phase boundaries, repo structure)
    ├── development_workflow.md        # Three-agent workflow and session procedures
    ├── COWORK_PROJECT_INSTRUCTIONS.md # Cowork project instructions
    ├── plans/
    │   ├── product-vision-draft.md    # Product brief (source of truth, 18 sections)
    │   └── design-phase-notes.md      # Deferred technical questions (10 sections)
    ├── adr/                           # Architectural decision records (empty — ready for use)
    ├── prompts/
    │   ├── session-start-prompt.md
    │   ├── fresh-agent-audit-prompt.md
    │   ├── cowork-summary-prompt.md
    │   ├── cowork-architecture-review-prompt.md
    │   ├── desktop-claude-summary-prompt.md
    │   ├── desktop-claude-review-prompt.md
    │   ├── vscode-claude-summary-prompt.md
    │   ├── product-brief-stress-test-prompt.md
    │   └── final-brief-alignment-check-prompt.md
    └── summaries/
        ├── cowork-summary.md
        ├── desktop-claude-summary.md
        └── vscode-claude-summary.md
```

---

## Implemented Features

None yet. The project is in the documentation and architecture phase.

---

## Not Implemented Yet

Everything. See `docs/architecture.md` for the target structure and `PROJECT_STATE.md` for next steps.

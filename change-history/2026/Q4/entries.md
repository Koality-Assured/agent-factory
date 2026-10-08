# Change history — 2026 Q4

Entries newest first. Append via `python scripts/change-history/append_change_history.py` only.

## Entries


### 2026-10-08 — Prevent local data loss during worktree cleanup

- **Requesting user:** Repository maintainer
- **AI agent:** Codex harness-operator
- **User request:** Make cleanup selectors exclusive and preserve ignored or untracked worktree data.
- **Summary:**
  - Reject mixed cleanup selectors and verify exact merged branch/PR head before targeted removal.
  - Refuse ignored or untracked local paths, report paths only, and keep the guard active under --force.

### 2026-10-08 — Add QA opportunity discovery

- **Requesting user:** Robbie
- **AI agent:** harness-operator
- **User request:** Add selectable opportunity discovery or problem finding and automatic executive triage for evidence-backed opportunities.
- **Summary:**
  - Added run objectives, opportunity evidence and success criteria, and prioritized ledger statuses; updated QA and executive contracts.


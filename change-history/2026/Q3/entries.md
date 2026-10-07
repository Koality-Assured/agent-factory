# Change history — 2026 Q3

Entries newest first. Append via `python scripts/change-history/append_change_history.py` only.

## Entries



### 2026-09-24 — Add Julian project coordinator

- **Requesting user:** Robbie
- **AI agent:** harness-operator
- **User request:** add a project coordinator who deconflicts batches and validates merges before a human merges
- **Summary:**
  - Added julian AGENT.md (model_tier high) with deconflict-batch and validate-merge skills
  - Promotion order is now Adrian assign, Julian deconflict, Leo, Kenji (the product target local replay), Nadia, Simone PR, Julian validate, human merge
  - Updated executive-triage, implement-finding, review-and-pr, staging-prove, and the calling harness factory project spec roster spec

### 2026-09-24 — Retarget first scenario pack to a private product target

- **Requesting user:** Robbie
- **AI agent:** harness-operator
- **User request:** retarget first factory scenario pack to a private product target and defer cadence for a manual kickoff
- **Summary:**
  - Replaced routing-surface scenario pack with product-target (game checkout target, playable UI/game-state, read-only personas)
  - Updated qa skill SoT links and default pack id to product-target; qa-schedule and executive-schedule cadence remains UNSET with manual invocation
  - Did not arm cron or invent an interval

### 2026-09-24 — Factory roster steps 2-6 partial

- **Requesting user:** Robbie
- **AI agent:** harness-operator
- **User request:** Implement agent-factory build-order steps 2-5 and partial 6 (agents, skills, scenario pack, run-lock, schedule stubs)
- **Summary:**
  - Added ten factory specialists with qa/ and executive/ skills
  - Added routing-surface scenario pack, run-lock contract, schedule stubs with cadence UNSET
  - Registered results/qa family; regenerated routing indexes


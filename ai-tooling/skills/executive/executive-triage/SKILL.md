---
schema_version: "2.0.0"
name: executive-triage
description: >-
  Read the factory ledger, assign a small batch, hand it to Julian for deconflict, then advance work items down the fixed promotion path. Optionally send one item back one step with one specific question. Use when Adrian runs an executive batch. Does not implement. Do not use to open PRs or skip gates.
owner_agent: adrian
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  delegated_skills:
    - deconflict-batch
    - implement-finding
    - staging-prove
    - security-intent-gate
    - review-and-pr
    - validate-merge
contracts:
  inputs:
    - Ledger path with open items
    - Run-lock state
  outputs:
    - Assignments through julian/leo/kenji/nadia/simone with gate stage
    - At most one backward-send; an executive run may take every open ledger item
---

# Executive Triage

## When to use

Ledger has open items and an executive batch should start (Adrian).

## When not to use

Implementing changes, opening PRs, or starting a QA persona sweep.

## Criticality

High: owns promotion order and run-lock. MUST NOT skip Nadia or Simone. MUST NOT skip Julian deconflict before Leo or Julian validate-merge after Simone's PR.

## Source of truth

- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-lock.md`](../../../../docs/standards/run-lock.md)
- Promotion order: 1 Adrian assigns → 2 Julian deconflicts → 3 Leo implements → 4 Kenji proves → 5 Nadia → 6 Simone (PR only) → 7 Julian validates → 8 human merge

## Isolation

`read-only` against the promotion target. Updates ledger metadata under `results/qa/` only. Honors run-lock.

## How to use

1. Read [`docs/standards/run-lock.md`](../../../../docs/standards/run-lock.md). If another executive batch holds the lock, or claimed pages overlap, **stop**.
2. Acquire the run lock for this batch. Select every open ledger item.
3. Assign by fixed order only:
   1. Adrian assigns every open ledger item.
   2. Julian deconflicts them into work items (`deconflict-batch`) so two items do not edit the same files at once.
   3. Leo implements each work item on a branch in an isolated worktree (`implement-finding`).
   4. Kenji proves it (`staging-prove`). Kenji follows the run-spec proof_mode (staging host or local replay). Do not invent a staging server.
   5. Nadia checks intent and security (`security-intent-gate`) — **cannot be skipped**.
   6. Simone reviews and is the **only** agent who may open the PR toward main (`review-and-pr`).
   7. Julian validates completeness and mergeability (`validate-merge`).
   8. A human merges.
4. Adrian may send **one** item backward **one** step with **one** specific question. MUST NOT skip Nadia, Simone, or Julian's gates.
5. Spawn specialists clean-slate with paths only; A2A default 8 exchanges. Do not implement.
6. Release or hand off the run lock when the batch ends.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill executive-triage --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT implement. MUST NOT skip Nadia, Simone, or Julian. Human merges only.

## Completion gates

Assignments recorded; run-lock respected; no promotion-target edits by Adrian.

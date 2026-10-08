---
schema_version: "2.0.0"
name: executive-triage
description: >-
  Read the factory ledger, automatically prioritize open defects, abuse findings, and evidenced opportunities, route a bounded batch to Julian for deconflict, and advance assigned work down the fixed promotion path. Defer lower-priority work with a reason. Use when Adrian runs an executive batch. Does not implement. Do not use to open PRs or skip gates.
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
    - Ledger path with open items and any previously deferred items eligible for reprioritization
    - Run-lock state
  outputs:
    - Priorities and assigned or deferred status for every open item, plus work routing through julian/leo/kenji/nadia/simone
    - At most one backward-send; every open item is triaged without a human-acceptance gate
---

# Executive Triage

## When to use

Ledger has open or deferred items and an executive batch should start (Adrian). Valid opportunity findings are eligible automatically; human acceptance is not a triage state.

## When not to use

Implementing changes, opening PRs, or starting a QA persona sweep.

## Criticality

High: owns promotion order, priority, ledger triage states, and run-lock. MUST NOT skip Nadia or Simone. MUST NOT skip Julian deconflict before Leo or Julian validate-merge after Simone's PR.

## Source of truth

- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-lock.md`](../../../../docs/standards/run-lock.md)
- Promotion order: 1 Adrian assigns → 2 Julian deconflicts → 3 Leo implements → 4 Kenji proves → 5 Nadia → 6 Simone (PR only) → 7 Julian validates → 8 human merge

## Isolation

`read-only` against the promotion target. Updates ledger metadata under `results/qa/` only. Honors run-lock.

## How to use

1. Read [`docs/standards/run-lock.md`](../../../../docs/standards/run-lock.md). If another executive batch holds the lock, or claimed pages overlap, **stop**.
2. Acquire the run lock for this batch. Review every `open` ledger item and every previously `deferred` item, including `opportunity` findings and historical `power-user-preference` entries.
3. Validate each item against [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md). For a historical `power-user-preference`, reclassify it as `opportunity` only if target evidence, impact, and testable success criteria are available; otherwise mark it `rejected` with a reason. Do not wait for human acceptance.
4. Prioritize every valid open or deferred item as `P0`–`P3` using observed reach, impact, urgency, and evidence quality. Send a bounded, highest-priority batch through the fixed order. Mark valid items held for capacity as `deferred` with a reason; they remain eligible for a later batch. Julian marks chosen items `assigned` after recording the deconflicted work items. Set a resulting triage status on every reviewed eligible item; never leave an item waiting for human acceptance.
5. Assign by fixed order only:
   1. Adrian prioritizes all open items and routes the selected batch.
   2. Julian deconflicts the selected findings into work items (`deconflict-batch`) so two items do not edit the same files at once.
   3. Leo implements each work item on a branch in an isolated worktree (`implement-finding`).
   4. Kenji proves it (`staging-prove`). Kenji follows the run-spec proof_mode (staging host or local replay). Do not invent a staging server.
   5. Nadia checks intent and security (`security-intent-gate`) — **cannot be skipped**.
   6. Simone reviews and is the **only** agent who may open the PR toward main (`review-and-pr`).
   7. Julian validates completeness and mergeability (`validate-merge`).
   8. A human merges.
6. Adrian may send **one** item backward **one** step with **one** specific question. MUST NOT skip Nadia, Simone, or Julian's gates. Missing opportunity evidence is a reason to reject or send for evidence gathering; it is not a human-acceptance gate.
7. Spawn specialists clean-slate with paths only; A2A default 8 exchanges. Do not implement.
8. Mark findings `closed` only after the normal promotion path completes and the human merge occurs. Release or hand off the run lock when the batch ends.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill executive-triage --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT implement. MUST NOT skip Nadia, Simone, or Julian. Human merges only.

## Completion gates

Every reviewed open or deferred item has a resulting assigned, deferred, or rejected status; valid items have priority, deferred/rejected items have a reason, selected items have deconflicted assignments; run-lock respected; no promotion-target edits by Adrian; no human-acceptance state.

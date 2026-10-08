---
schema_version: "2.0.0"
name: deconflict-batch
description: >-
  Take Adrian's prioritized ledger batch, including opportunities, and split or sequence it so two items do not edit the same files at once. Record work items before Leo starts. Use when Julian deconflicts an executive batch. Does not implement. Do not open PRs or merge.
owner_agent: julian
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
contracts:
  inputs:
    - Adrian's prioritized batch of open ledger findings, including opportunities
    - Claimed or likely file paths per finding when known
  outputs:
    - Recorded work items split or sequenced with no overlapping concurrent file edits and selected findings marked assigned
---

# Deconflict Batch

## When to use

Adrian has prioritized open ledger items and selected a batch; Julian must turn selected defect, abuse, and opportunity findings into non-overlapping work items before Leo starts.

## When not to use

Implementing changes, opening PRs, merge validation after Simone, or QA persona sweeps.

## Criticality

High: prevents concurrent edits to the same files. Leo must not start until work items are recorded.

## Source of truth

- Owner `ai-tooling/agents/julian/AGENT.md`
- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-lock.md`](../../../../docs/standards/run-lock.md)
- Adrian's batch assignment

## Isolation

`read-only` against the product target. Records work items under `results/qa/` only.

## How to use

1. Read Adrian's prioritized batch and each finding's likely touch set (paths from the finding, claim, or `qmd search` / bounded reads — no tree walks).
2. Split or sequence so two items do not edit the same files at once. Prefer sequencing when overlap is unavoidable; prefer parallel work items when disjoint.
3. Record work items (id, source finding ids, ordered/parallel group, claimed paths, and a pointer to the finding's expected result or opportunity `success_criteria`) under `results/qa/`.
4. Mark selected findings `triage_status: assigned` after their work items are recorded; return item ids and assignments to Adrian.
5. Return the work-item list to Adrian. Do **not** implement. Do **not** open a PR. Do **not** merge. Leo starts only after this step.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill deconflict-batch --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT implement. MUST NOT open PRs. MUST NOT merge.

## Completion gates

Work items recorded with no concurrent overlapping file edits; Leo not started by Julian.

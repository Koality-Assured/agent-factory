---
schema_version: "2.0.0"
name: qa-run
description: >-
  Start a factory QA run for problems, opportunities, or both; omission keeps the existing problem-finding sweep. Spawn the applicable personas clean-slate, validate and dedupe findings into the ledger, and store at most one follow-up. Use when Mara starts a QA sweep. Do not use for executive promotion or promotion-target edits.
owner_agent: mara
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  delegated_skills:
    - incompetent-user-find
    - regular-user-find
    - competent-user-find
    - abuse-test
contracts:
  inputs:
    - Run id, target path or host, scenario pack path, optional objective (`problems`, `opportunities`, or `both`; defaults to `problems`)
  outputs:
    - Private run record under results/qa/runs/<run-id>/
    - Deduped, schema-valid ledger entries marked open for automatic triage; optional one follow-up question
---

# Qa Run

## When to use

Starting or continuing a factory QA run as Mara with a run id, target, scenario pack, and optional objective.

## When not to use

Executive promotion, implementing fixes, opening PRs, or editing the promotion target.

## Criticality

High: orchestrates all QA personas; findings without reproduction MUST be dropped.

## Source of truth

- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- [`docs/qa/scenario-packs/_template.md`](../../../../docs/qa/scenario-packs/_template.md)
- [`ai-tooling/a2a/interaction-protocol.md`](../../../a2a/interaction-protocol.md) (8-exchange default; clean-slate spawns)

## Isolation

`read-only` against the target. Writes only under `results/qa/`. Parent does not load this SKILL.md body to dispatch — spawn Mara with paths.

## How to use

1. Accept a complete [run spec](../../../../docs/standards/run-spec.md): `run_id`, `target`, and `pack_id` or `pack_path`. Fail closed if any required field is missing. If `objective` is omitted, use `problems`; otherwise accept only `problems`, `opportunities`, or `both`. Discover pack via `qmd search` / `qmd get` if only a name is given — no tree walks. There is **no default pack**.
2. Create private run record at `results/qa/runs/<run_id>/` and open the shared ledger under `results/qa/ledger/`.
3. If a stored follow-up question names one persona and the same objective, spawn **only** that persona clean-slate with the question. Keep a follow-up queued when its objective differs or its persona is not part of this objective. Otherwise, for `opportunities`, spawn **owen**, **priya**, and **elena**; for `problems` or `both`, spawn all four personas, including **marcus**. Pass the objective, target, scenario pack, `AGENT.md` and `SKILL.md` paths only; do not pass prior transcripts. A2A budget: 8 exchanges each.
4. Collect findings for the selected objective only and require every new finding's `objective` to match the run spec. In `problems`, accept defect and abuse findings; in `opportunities`, accept opportunity findings; in `both`, accept each class separately. Drop findings without actionable reproduction. An opportunity also requires specific evidence, user impact, and testable `success_criteria` under the [finding schema](../../../../docs/standards/finding-schema.md). Omit unsupported feature ideas and taste-only preferences. Cap Owen at five before dedupe.
5. For Marcus: keep raw abuse evidence only in `results/qa/runs/<run_id>/private/`; put schema-valid abuse finding summaries (no attack recipe) into the ledger.
6. Dedupe into the ledger by reproduced defect, abuse case, or evidenced unmet need; set each valid new item to `triage_status: open`. At most one incomplete finding may store one self-contained follow-up question, together with its persona and objective, for a later matching sweep. Drop an item that remains unsupported; do not hold valid findings for human acceptance.
7. Stop. Do not edit the promotion target or assign executive work. Valid open findings are eligible for automatic executive triage.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill qa-run --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT edit the promotion target. MUST NOT pass prior transcripts to personas. Abuse evidence stays private.

## Completion gates

Ledger updated with the selected objective and valid findings marked open; private run record path returned; no promotion-target mutations or human-acceptance gate.

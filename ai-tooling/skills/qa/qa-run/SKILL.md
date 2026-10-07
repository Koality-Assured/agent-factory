---
schema_version: "2.0.0"
name: qa-run
description: >-
  Start a factory QA run: accept run id, target, and scenario pack; spawn the four user personas clean-slate in parallel; dedupe findings into the ledger; store at most one follow-up. Use when Mara starts a QA sweep. Do not use for executive promotion or promotion-target edits.
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
    - Run id, target path or host, scenario pack path
  outputs:
    - Private run record under results/qa/runs/<run-id>/
    - Deduped ledger entries; optional one follow-up question
---

# Qa Run

## When to use

Starting or continuing a factory QA run as Mara with a run id, target, and scenario pack.

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

1. Accept a complete [run spec](../../../../docs/standards/run-spec.md): `run_id`, `target`, and `pack_id` or `pack_path`. Fail closed if any required field is missing. Discover pack via `qmd search` / `qmd get` if only a name is given — no tree walks. There is **no default pack**.
2. Create private run record at `results/qa/runs/<run_id>/` and open the shared ledger under `results/qa/ledger/`.
3. If this is a follow-up sweep and the ledger stores one self-contained question for one persona: spawn **only** that persona clean-slate with the question. Else spawn **owen**, **priya**, **elena**, and **marcus** in parallel, clean-slate, with no prior transcript. Pass `AGENT.md` and `SKILL.md` paths only. A2A budget: 8 exchanges each.
4. Collect findings. Drop any without `reproduction`. Cap Owen at five before dedupe. Class Elena overbuilt ideas as `power-user-preference`.
5. For Marcus: keep raw abuse evidence only in `results/qa/runs/<run_id>/private/`; put schema-valid abuse finding summaries (no attack recipe) into the ledger.
6. Dedupe into the ledger. At most one incomplete finding may store one self-contained follow-up question for a later sweep. A second miss on the same question stays blocked for a human.
7. Stop. Do not edit the promotion target. Do not assign executive work.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill qa-run --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT edit the promotion target. MUST NOT pass prior transcripts to personas. Abuse evidence stays private.

## Completion gates

Ledger updated; private run record path returned; no promotion-target mutations.

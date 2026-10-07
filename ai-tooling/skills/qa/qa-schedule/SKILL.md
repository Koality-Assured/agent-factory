---
schema_version: "2.0.0"
name: qa-schedule
description: >-
  Schedule stub that starts Mara for a factory QA run. Use when wiring or documenting the QA schedule. Cadence is UNSET — do not invent an interval. Do not use to run executive promotion.
owner_agent: mara
rank: medium
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  delegated_skills:
    - qa-run
contracts:
  inputs:
    - Operator run spec (run id, target, pack id or path, mode); no product default
  outputs:
    - Dispatch plan that starts Mara with qa-run inputs; cadence field left UNSET
---

# Qa Schedule

## When to use

Defining or invoking the QA schedule entrypoint that starts Mara.

## When not to use

Picking a cron interval, arming a host scheduler, or starting Adrian.

## Criticality

Medium: schedule contract only. Cadence is deferred (**UNSET**) until a human sets it. Invocation is **manual** — first run is a manual kickoff. Do not invent an interval or arm cron.

## Source of truth

- This skill
- `qa-run`
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- [`docs/qa/scenario-packs/_template.md`](../../../../docs/qa/scenario-packs/_template.md)

## Isolation

`read-only`. Does not arm cron. Does not mutate the promotion target.

## How to use

1. Confirm cadence is **UNSET** (deferred). Invocation is manual. Do not choose an interval.
2. Build the start payload for Mara from the operator [run spec](../../../../docs/standards/run-spec.md): `run_id`, `target`, `pack_id` or `pack_path`, and `mode`. Fail closed if any required field is missing. There is **no default pack**.
3. Spawn Mara with `qa-run` paths only (clean-slate). Do not start Adrian from this skill.
4. Return the dispatch plan. Do not install or enable a host scheduler.

## Dry run

Read this skill and confirm cadence is UNSET; `python scripts/ai-tooling/validate_skill.py --skill qa-schedule --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

Do not arm cron. Do not store secrets in schedule config.

## Completion gates

Dispatch plan documented; cadence still UNSET; no scheduler armed.

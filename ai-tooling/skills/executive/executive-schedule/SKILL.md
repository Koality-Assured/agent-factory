---
schema_version: "2.0.0"
name: executive-schedule
description: >-
  Schedule stub that starts Adrian only when the ledger has open items. Use when wiring or documenting the executive schedule. Cadence is UNSET — do not invent an interval. Do not use to start Mara or arm cron.
owner_agent: adrian
rank: medium
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  delegated_skills:
    - executive-triage
contracts:
  inputs:
    - Ledger path
    - Run-lock state
  outputs:
    - Dispatch plan that starts Adrian when open items exist; cadence field left UNSET
    - No-op decision when ledger has no open items
---

# Executive Schedule

## When to use

Defining or invoking the executive schedule entrypoint that may start Adrian.

## When not to use

Picking a cron interval, arming a host scheduler, or starting Mara.

## Criticality

Medium: schedule contract only. Cadence is deferred (**UNSET**) until a human sets it. Invocation is **manual** — first run is a manual kickoff. Do not invent an interval or arm cron.

## Source of truth

- This skill
- `executive-triage`
- [`docs/standards/run-lock.md`](../../../../docs/standards/run-lock.md)

## Isolation

`read-only`. Does not arm cron. Does not mutate the promotion target.

## How to use

1. Confirm cadence is **UNSET** (deferred). Invocation is manual. Do not choose an interval.
2. Inspect the ledger for open items. If none, return a no-op.
3. Check [`docs/standards/run-lock.md`](../../../../docs/standards/run-lock.md). If locked or page overlap would occur, return blocked.
4. Otherwise spawn Adrian with `executive-triage` paths only (clean-slate).
5. Do not install or enable a host scheduler.

## Dry run

Read this skill and confirm cadence is UNSET; `python scripts/ai-tooling/validate_skill.py --skill executive-schedule --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

Do not arm cron. Do not start Adrian when the ledger is empty.

## Completion gates

Dispatch plan or no-op; cadence still UNSET; no scheduler armed.

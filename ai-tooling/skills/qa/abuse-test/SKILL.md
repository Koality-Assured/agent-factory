---
schema_version: "2.0.0"
name: abuse-test
description: >-
  Factory abuse-tester pass against the run-spec target only. Use when Mara dispatches Marcus. No production credentials, no write tools; abuse evidence stays in the private run record. Do not use for promotion-target edits or out-of-target probing.
owner_agent: marcus
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
contracts:
  inputs:
    - Run id, designated target from run spec, scenario pack path, objective (`problems` or `both`)
  outputs:
    - Abuse-class schema findings for Mara
    - Raw evidence path under the private run record only
---

# Abuse Test

## When to use

Mara dispatches an abuse pass for a `problems` or `both` run, or a follow-up question targets Marcus.

## When not to use

Any write to the target / promotion target, production credential use, or targets outside the run spec.

## Criticality

High: misuse simulation with hard containment. Private-finding rule is non-negotiable.

## Source of truth

- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- Owner `ai-tooling/agents/marcus/AGENT.md`

## Isolation

`read-only`. No write tools. Stay inside the designated target.

## How to use

1. Confirm the designated target and objective from the run spec. Refuse if asked to leave the target or to run an abuse pass for `objective: opportunities`.
2. Attempt break/misuse scenarios from the pack only with read tools. No production credentials. No write tools.
3. Emit `class: abuse` findings with the selected `objective` and reproduction that Mara can re-check without publishing an attack recipe.
4. Put raw evidence exclusively under `results/qa/runs/<run_id>/private/` (Mara creates the folder). Do not put attack steps in the shared ledger.
5. Nadia later decides what is safe to turn into a durable change; the durable change is the control.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill abuse-test --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT leave the run-spec target. MUST NOT use production credentials or write tools. Abuse evidence stays private.

## Completion gates

Findings + private evidence pointer returned to Mara. No promotion-target writes.

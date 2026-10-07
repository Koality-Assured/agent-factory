---
schema_version: "2.0.0"
name: competent-user-find
description: >-
  Factory QA persona skill for elena. Use when Mara dispatches that persona against a target and scenario pack. Returns findings only. Do not use to edit the promotion target or open PRs.
owner_agent: elena
rank: medium
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
contracts:
  inputs:
    - Run id, target, scenario pack path, optional single follow-up question
  outputs:
    - Schema-valid findings with reproduction; invalid findings omitted
---

# Competent User Find

## When to use

Mara dispatches a competent-user pass, or a follow-up question targets Elena.

## When not to use

Promotion-target edits, executive promotion, or abuse testing (use `abuse-test`).

## Criticality

Medium: persona finding production. Findings without reproduction are invalid.

## Source of truth

- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- Owner `ai-tooling/agents/elena/AGENT.md`

## Isolation

`read-only` against the target. Return findings to Mara; do not write the ledger.

## How to use

1. Read the scenario pack via `qmd get` or a targeted read of the given path — no tree walks.
2. Exercise the target per persona scope. Use the target correctly, including advanced pack scenarios. Class overbuilt ideas as `power-user-preference` until a human accepts them — never as `defect`.
3. Emit findings matching [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md). Required fields: id, persona, target, what_they_tried, reproduction, expected_result, actual_result, class.
4. Omit any finding lacking actionable reproduction.
5. Return the Structured Result Envelope to Mara. Do not edit the promotion target.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill competent-user-find --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

Read-only. Preferences stay preferences until a human accepts them.

## Completion gates

Findings returned to Mara. No ledger or promotion-target writes.

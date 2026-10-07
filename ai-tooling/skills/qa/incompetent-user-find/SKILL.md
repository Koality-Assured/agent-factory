---
schema_version: "2.0.0"
name: incompetent-user-find
description: >-
  Factory QA persona skill for owen. Use when Mara dispatches that persona against a target and scenario pack. Returns findings only. Do not use to edit the promotion target or open PRs.
owner_agent: owen
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

# Incompetent User Find

## When to use

Mara dispatches an incompetent-user pass, or a follow-up question targets Owen.

## When not to use

Promotion-target edits, executive promotion, or abuse testing (use `abuse-test`).

## Criticality

Medium: persona finding production. Findings without reproduction are invalid.

## Source of truth

- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- Owner `ai-tooling/agents/owen/AGENT.md`

## Isolation

`read-only` against the target. Return findings to Mara; do not write the ledger.

## How to use

1. Read the scenario pack via `qmd get` or a targeted read of the given path — no tree walks.
2. Exercise the target per persona scope. Use the target wrong, get lost, try actions that should fail. Return at most **five** findings. Omit anything without reproduction.
3. Emit findings matching [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md). Required fields: id, persona, target, what_they_tried, reproduction, expected_result, actual_result, class.
4. Omit any finding lacking actionable reproduction.
5. Return the Structured Result Envelope to Mara. Do not edit the promotion target.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill incompetent-user-find --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

Read-only. Hard cap of five findings per run. Drop findings without reproduction.

## Completion gates

Findings returned to Mara. No ledger or promotion-target writes.

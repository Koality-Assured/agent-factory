---
schema_version: "2.0.0"
name: regular-user-find
description: >-
  Factory QA persona skill for priya. Use when Mara dispatches that persona against a target and scenario pack for problems, opportunities, or both. Returns findings only. Do not use to edit the promotion target or open PRs.
owner_agent: priya
rank: medium
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
contracts:
  inputs:
    - Run id, target, scenario pack path, objective, optional single follow-up question
  outputs:
    - Schema-valid findings with reproduction and opportunity evidence fields when applicable; invalid findings omitted
---

# Regular User Find

## When to use

Mara dispatches a regular-user pass for the selected run objective, or a follow-up question targets Priya.

## When not to use

Promotion-target edits, executive promotion, or abuse testing (use `abuse-test`).

## Criticality

Medium: persona finding production. Findings without reproduction are invalid.

## Source of truth

- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- Owner `ai-tooling/agents/priya/AGENT.md`

## Isolation

`read-only` against the target. Return findings to Mara; do not write the ledger.

## How to use

1. Read the scenario pack via `qmd get` or a targeted read of the given path — no tree walks.
2. Exercise the target per persona scope. Follow the obvious documented path in the scenario pack against the target. For `problems`, report reproducible defects; for `opportunities`, verify where a user goal is missing, blocked, or requires a meaningful workaround; for `both`, cover both. Record findings only.
3. Emit findings matching [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md), including the exact selected `objective`. Include the common required fields. For each `opportunity`, include specific `evidence`, user impact, and testable `success_criteria`.
4. Omit any finding lacking actionable reproduction.
5. Return the Structured Result Envelope to Mara. Do not edit the promotion target.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill regular-user-find --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

Read-only. No write tools against the target. Omit speculative opportunities and taste-only requests.

## Completion gates

Findings returned to Mara. No ledger or promotion-target writes.

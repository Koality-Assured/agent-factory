---
schema_version: "2.0.0"
name: incompetent-user-find
description: >-
  Factory QA persona skill for owen. Use when Mara dispatches that persona against a target and scenario pack for problems, opportunities, or both. Returns findings only. Do not use to edit the promotion target or open PRs.
owner_agent: owen
rank: medium
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
contracts:
  inputs:
    - Run id, target, scenario pack path, objective, optional single follow-up question
  outputs:
    - Up to five schema-valid findings with reproduction and opportunity evidence fields when applicable
---

# Incompetent User Find

## When to use

Mara dispatches an incompetent-user pass for the selected run objective, or a follow-up question targets Owen.

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
2. Exercise the target per persona scope. Use the target wrong, get lost, try actions that should fail. For `problems`, report reproducible defects; for `opportunities`, note task attempts that cannot be completed without a concrete workaround or repeated friction; for `both`, cover both. Return at most **five** findings across all classes. Omit anything without reproduction.
3. Emit findings matching [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md), including the exact selected `objective`. Include the common required fields. For each `opportunity`, include specific `evidence`, user impact, and testable `success_criteria`.
4. Omit any finding lacking actionable reproduction.
5. Return the Structured Result Envelope to Mara. Do not edit the promotion target.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill incompetent-user-find --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

Read-only. Hard cap of five findings per run. Drop findings without reproduction and opportunities without evidence, impact, or testable success criteria.

## Completion gates

Findings returned to Mara. No ledger or promotion-target writes.

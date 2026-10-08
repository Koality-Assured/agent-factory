---
schema_version: "2.0.0"
name: competent-user-find
description: >-
  Factory QA persona skill for elena. Use when Mara dispatches that persona against a target and scenario pack for problems, opportunities, or both. Returns findings only. Do not use to edit the promotion target or open PRs.
owner_agent: elena
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

# Competent User Find

## When to use

Mara dispatches a competent-user pass for the selected run objective, or a follow-up question targets Elena.

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

1. Read the scenario pack via `qmd get` or a targeted read of the given path — no tree walks. Apply the run-spec objective (`problems` if absent).
2. Exercise the target correctly, including advanced pack scenarios. For `problems`, report reproducible defects only. For `opportunities`, identify concrete unmet tasks, capability gaps, or repeated workarounds and verify them against the target. For `both`, keep the two classes distinct. Never label a preference as a defect.
3. Emit findings matching [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md), including the exact selected `objective`. Include the common required fields. For each `opportunity`, include concrete `evidence`, affected workflow and consequence in `impact`, and observable `success_criteria`.
4. Omit any finding lacking actionable reproduction. Omit any opportunity supported only by taste, speculation, or an unverified assumption.
5. Return the Structured Result Envelope to Mara. Do not edit the promotion target.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill competent-user-find --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

Read-only. Do not wait for human acceptance. Convert a preference into an opportunity only when observed task evidence, impact, and testable success criteria meet the finding schema; otherwise omit it.

## Completion gates

Findings returned to Mara. No ledger or promotion-target writes.

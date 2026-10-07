---
schema_version: "2.0.0"
name: security-intent-gate
description: >-
  Required security and intent gate after Kenji proof (local-replay and/or declared staging per run-spec proof_mode). Use when Adrian advances an item to Nadia. Blocks work that conflicts with stated intent or weakens security; decides promotion-safe controls. Cannot be skipped.
owner_agent: nadia
rank: critical
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  required_skills:
    - staging-prove
contracts:
  inputs:
    - Work item, Kenji proof (per run-spec proof_mode), optional private abuse summary
  outputs:
    - Pass, block, or pass-with-promotion-safe-control
---

# Security Intent Gate

## When to use

Kenji has passed proof for the run-spec `proof_mode` and Adrian advances to Nadia.

## When not to use

Any path that skips Kenji, opens a PR, or publishes raw abuse steps to the promotion target.

## Criticality

Critical: cannot be skipped. The durable change is the control for abuse findings.

## Source of truth

- Owner `ai-tooling/agents/nadia/AGENT.md`
- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- Kenji proof artifact

## Isolation

`read-only`. Gate decision only. Does not implement or open PRs.

## How to use

1. Refuse if Kenji proof is missing or does not match the run-spec `proof_mode` (accept local-replay and/or declared staging; do not invent hosts).
2. Check stated intent vs the change. Block on intent conflict or security weakening.
3. For abuse-derived items: decide the promotion-safe control text. Do not paste attack recipes. The durable change is the control.
4. Record pass / block / pass-with-promotion-safe-control on the work item for Simone.
5. Return to Adrian. MUST NOT be bypassed.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill security-intent-gate --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT skip. MUST NOT approve without Kenji proof. MUST NOT publish raw abuse steps into promotion-bound content.

## Completion gates

Gate decision recorded; Simone must not proceed without a pass.

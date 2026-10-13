---
schema_version: "2.0.0"
name: security-intent-gate
description: >-
  Required security, intent, and blind adversarial review gate after Kenji proof. Evaluates changes blind to author rationale to eliminate cognitive bias. Blocks work that conflicts with stated intent or weakens security; decides promotion-safe controls. Use when Adrian advances an item to Nadia after Kenji proof. Cannot be skipped.
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
    - Work item, Kenji proof (per run-spec proof_mode and target_commit_sha), raw code diff, optional private abuse summary
  outputs:
    - Pass, block, or pass-with-promotion-safe-control
---

# Security Intent Gate

## When to use

Kenji has passed proof for the run-spec `proof_mode` (with valid `target_commit_sha`) and Adrian advances to Nadia.

## When not to use

Any path that skips Kenji, opens a PR, or publishes raw abuse steps to the promotion target.

## Criticality

Critical: cannot be skipped. Evaluates raw diffs blind to author rationale. The durable change is the control for abuse findings.

## Source of truth

- Owner `ai-tooling/agents/nadia/AGENT.md`
- [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- Kenji proof artifact (`proof.json`)

## Isolation

`read-only`. Gate decision only. Does not implement or open PRs.

## How to use

1. Refuse if Kenji proof is missing, invalid, or does not match the run-spec `proof_mode` (accept local-replay and/or declared staging; do not invent hosts).
2. Conduct **blind adversarial review**: inspect raw diffs and test cases *without* Leo's self-justifying rationales or defensive commentary. Evaluate boundary conditions, concurrency/lease edges, privilege boundaries, and stated architectural intent objectively.
3. Enforce **cross-model diversity**: Nadia executes on a secondary model family (e.g. Claude) distinct from Leo's primary model family (Gemini).
4. For abuse-derived items: decide the promotion-safe control text. Do not paste attack recipes. The durable change is the control.
5. Record pass / block / pass-with-promotion-safe-control on the work item for Simone's adjudication pass.
6. Return findings and gate decision to Adrian. MUST NOT be bypassed.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill security-intent-gate --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT skip. MUST NOT approve without Kenji proof. MUST NOT publish raw abuse steps into promotion-bound content.

## Completion gates

Gate decision recorded; Simone must not proceed without a pass.

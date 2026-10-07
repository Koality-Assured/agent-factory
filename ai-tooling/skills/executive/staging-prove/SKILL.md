---
schema_version: "2.0.0"
name: staging-prove
description: >-
  Prove that Leo's change does what Leo claims before Nadia. Use when Adrian advances an item
  to Kenji after Leo implements. Prefer staging when the run spec provides a host; otherwise
  locally replay the finding reproduction on Leo's branch. Do not invent a staging server.
  Do not open PRs or skip this gate.
owner_agent: kenji
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
contracts:
  inputs:
    - Work item, Leo branch/worktree, claimed behavior, run-spec proof mode
  outputs:
    - Proof artifact (staging or local replay) or fail with reproduction
---

# Staging Prove

## When to use

Adrian advances an item to Kenji after Leo's implementation.

## When not to use

Implementing product changes, opening PRs, inventing a staging host, or replacing Nadia's gate.

## Criticality

High: required before Nadia. Proof is mandatory. Use the run-spec `proof_mode`; do not invent infrastructure the run spec does not name.

## Source of truth

- Owner `ai-tooling/agents/kenji/AGENT.md`
- Leo claim summary
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)

## Isolation

`read-only` against production. Staging-only credentials when provided by run spec. Without a staging host, proof is local on Leo's branch.

## How to use

1. Read Leo's claimed behavior and the run-spec proof mode. Discover verification notes via `qmd search` when needed.
2. If the run spec provides a staging host (`proof_mode: staging`), prove the claim there. Never use production credentials.
3. If the run spec says `local-replay` or provides no staging host: locally replay the finding reproduction on Leo's branch/worktree. Do **not** invent a staging server.
4. Write proof under `results/qa/runs/<run_id>/staging/` (or `.../proof/` for local replay) or fail with reproduction.
5. Return pass/fail to Adrian. Do not open a PR. Do not call Nadia's decision.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill staging-prove --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

No production credentials. No PR. No merge.

## Completion gates

Staging proof or local-replay proof recorded; Nadia not skipped by implication.

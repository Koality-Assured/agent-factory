---
schema_version: "2.0.0"
name: review-and-pr
description: >-
  Review Leo's work after Nadia passes and open the pull request toward main. Use when Adrian advances an item to Simone. Only agent who may open that PR. Julian validates next; a human merges. Do not merge.
owner_agent: simone
rank: high
isolation: mutate
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  required_skills:
    - security-intent-gate
contracts:
  inputs:
    - Work item, Leo branch, Kenji proof, Nadia pass
  outputs:
    - Review result; PR URL on pass; never a merge
---

# Review And Pr

## When to use

Nadia has passed and Adrian assigns Simone to review and open the PR.

## When not to use

Merging to main, skipping Nadia, validating mergeability (Julian), or opening a PR without Kenji+Nadia clearance.

## Criticality

High: Simone is the only agent who may open the PR toward main. Julian then validates completeness and mergeability. A human merges.

## Source of truth

- Owner `ai-tooling/agents/simone/AGENT.md`
- `github-workflow` patterns via qmd
- Gate artifacts

## Isolation

`mutate` in the isolated worktree for review-only fixes if assigned. Opens PR; never merges.

## How to use

1. Refuse without Kenji proof and Nadia pass on the work item.
2. Review Leo's branch. Request changes via Adrian backward-send if needed (do not skip gates).
3. On pass: open the pull request toward `main` with Conventional Commits title. Simone is the **only** agent who may open this PR.
4. Do **not** merge. Hand the PR to Julian (`validate-merge`) for completeness and mergeability. A human merges after Julian passes.
5. Return PR URL or block reason to Adrian. An executive run may open one pull request per deconflicted work item.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill review-and-pr --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT merge. MUST NOT open PR without Kenji and Nadia. No secrets in PR body.

## Completion gates

PR opened or blocked; Julian validate-merge next; human merge remaining; run-lock pages still claimed until merge/release.

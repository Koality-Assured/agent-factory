---
schema_version: "2.0.0"
name: review-and-pr
description: >-
  Adjudicate review findings (accept/reject/defer), apply accepted fixes, verify Kenji's commit SHA proof validity, and open the pull request toward main with standardized git provenance trailers. Use when Adrian advances an item to Simone after Nadia passes. Only agent who may open that PR. Julian validates next; a human merges. Do not merge.
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
    - Work item, Leo branch, Kenji proof artifact (with target_commit_sha), Nadia pass
  outputs:
    - Adjudication log, review result, and PR URL on pass; never a merge
---

# Review And Pr

## When to use

Nadia has passed and Adrian assigns Simone to adjudicate findings, review, and open the PR.

## When not to use

Merging to main, skipping Nadia, validating mergeability (Julian), or opening a PR without valid Kenji+Nadia clearance and matching commit SHA proof.

## Criticality

High: Simone is the only agent who may open the PR toward main. Julian then validates completeness and mergeability. A human merges.

## Source of truth

- Owner `ai-tooling/agents/simone/AGENT.md`
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- `github-workflow` patterns via qmd
- Gate artifacts (Kenji proof.json, Nadia pass)

## Isolation

`mutate` in the isolated worktree for review-only fixes if assigned. Opens PR; never merges.

## How to use

1. Refuse without Kenji proof and Nadia pass on the work item. Verify Kenji's `target_commit_sha` matches the branch tip commit SHA.
2. Adjudicate all findings from Nadia and code review in an explicit adjudication log:
   - **`accepted`**: Apply fix to the branch. *Applying fixes amends the commit tree and changes the branch tip SHA, which immediately invalidates Kenji's proof and mandates re-running Kenji's proof before opening the PR.*
   - **`rejected`**: Document technical rationale explaining why the finding does not apply.
   - **`deferred`**: Bounded as non-blocking technical debt for a subsequent run.
3. On pass and with verified matching `target_commit_sha` proof: open the pull request toward `main` with Conventional Commits title and standardized git provenance trailers:
   ```gitcommit
   Co-Authored-By: Agent Factory <agent-factory@local>
   X-Factory-Run: <run_id>
   X-Factory-Ledger-ID: <finding_id>
   ```
   Simone is the **only** agent who may open this PR.
4. Do **not** merge. Hand the PR to Julian (`validate-merge`) for completeness, mergeability, and git ancestry checks. A human merges after Julian passes.
5. Return PR URL or block reason to Adrian. An executive run may open one pull request per deconflicted work item.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill review-and-pr --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT merge. MUST NOT open PR without Kenji and Nadia. No secrets in PR body.

## Completion gates

PR opened or blocked; Julian validate-merge next; human merge remaining; run-lock pages still claimed until merge/release.

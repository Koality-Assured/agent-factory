---
schema_version: "2.0.0"
name: validate-merge
description: >-
  After Simone opens the pull request, check the diff against each assigned finding's expected result or opportunity success criteria, verify server-side git ancestry (git merge-base --is-ancestor) against Kenji's proof commit SHA, confirm tier compliance, and confirm the PR is mergeable with no base-branch conflicts. Use when Julian validates completeness and mergeability. Report pass or fail. Does not merge. A human still merges.
owner_agent: julian
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
  - git
contracts:
  inputs:
    - PR URL or number, deconflicted work items, finding expected results or opportunity success criteria, Kenji proof artifact (with target_commit_sha)
  outputs:
    - Completeness, ancestry, and mergeability pass or fail report; never a merge
---

# Validate Merge

## When to use

Simone has opened the pull request toward main and Julian must validate completeness, git ancestry, and mergeability before a human merges.

## When not to use

Deconflicting Adrian's batch, implementing, opening the PR, or merging to main.

## Criticality

High: last agent gate before human merge. Partial fixes must fail. Broken git ancestry must fail. Conflicts with base must fail.

## Source of truth

- Owner `ai-tooling/agents/julian/AGENT.md`
- Deconflicted work items from `deconflict-batch`
- Finding expected results per [`docs/standards/finding-schema.md`](../../../../docs/standards/finding-schema.md)
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)
- Kenji proof artifact (`proof.json`)
- Simone's PR

## Isolation

`read-only`. Inspects PR/diff and ledger artifacts. Does not merge.

## How to use

1. Load the deconflicted work items, assigned finding expected results, and Kenji's `proof.json`.
2. Inspect the pull request diff. For each finding, confirm the change set meets its expected result or all opportunity success criteria. **Fail** the item if a finding is only partly addressed.
3. Verify server-side git ancestry: run `git merge-base --is-ancestor <target_commit_sha> <branch_tip>` to cryptographically verify that the commit tested by Kenji is an ancestor of the branch tip being promoted.
4. Verify standardized git provenance trailers: confirm commits contain `Co-Authored-By: Agent Factory <agent-factory@local>`, `X-Factory-Run`, and `X-Factory-Ledger-ID`.
5. Check the PR is mergeable: no conflicts with the base branch (`main` unless the run says otherwise). Confirm the change set matches the deconflicted work items (no surprise paths or dropped items).
6. Record pass or fail under `results/qa/` with short rationale per item.
7. Return pass/fail to Adrian. Do **not** merge. A human still merges.

## Dry run

`python scripts/ai-tooling/validate_skill.py --skill validate-merge --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

MUST NOT merge. MUST NOT open or rewrite the PR. Fail on partial fixes or base conflicts.

## Completion gates

Pass/fail recorded; human merge remaining; Julian did not merge.

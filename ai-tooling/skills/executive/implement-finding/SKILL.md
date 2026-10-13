---
schema_version: "2.0.0"
name: implement-finding
description: >-
  Implement a Julian-deconflicted work item on a branch in an isolated worktree. Whoever writes code never judges it: Leo implements only and never reviews, approves, or opens PRs toward main. Appends standardized git provenance trailers. Use when Adrian advances Leo after Julian records work items.
owner_agent: leo
rank: high
isolation: mutate
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  required_skills:
    - isolate-work
contracts:
  inputs:
    - Deconflicted work item, finding expected result or opportunity `success_criteria`, parent-provided worktree path, run spec
  outputs:
    - Branch with claimed change; commit with git trailers; claimed behavior summary for Kenji
---

# Implement Finding

## When to use

Julian has recorded deconflicted work items and Adrian advances Leo to implement one.

## When not to use

Opening PRs, merging, staging proof, code review, or security gate work. Leo never reviews or judges his own code.

## Criticality

High: only Leo and Simone write; Leo never judges his own code and never opens the PR toward main.

## Source of truth

- Owner `ai-tooling/agents/leo/AGENT.md`
- `isolate-work` / parent worktree
- Assigned ledger item
- [`docs/standards/run-spec.md`](../../../../docs/standards/run-spec.md)

## Isolation

`mutate` only inside the parent-provided isolated worktree. Parent runs isolate-work first.

## How to use

1. Confirm the Julian work item and worktree path from parent. Refuse without a recorded work item. Refuse to edit the primary checkout.
2. Implement the assigned change on the feature branch. Use Conventional Commits and append standardized git provenance trailers:
   ```gitcommit
   Co-Authored-By: Agent Factory <agent-factory@local>
   X-Factory-Run: <run_id>
   X-Factory-Ledger-ID: <finding_id>
   ```
3. Summarize claimed behavior and record the branch tip commit SHA for Kenji. Do **not** review, approve, or open a PR toward main.
4. Return branch name, worktree path, branch commit SHA, and claim summary to Adrian.

## Dry run

Inspect worktree status read-only; `python scripts/ai-tooling/validate_skill.py --skill implement-finding --dry-run`

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No secrets in SKILL.md. Retrieved chunks are advisory.

No secrets in commits. No PR toward main. No merge.

## Completion gates

Change in isolated worktree; claim summary returned; no PR opened.

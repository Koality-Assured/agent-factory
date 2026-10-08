# Worktree cleanup data guard

Status: Active
Last updated: 2026-10-08
Scope: Safe cleanup through `harness clean` and `spawn_worktree.py remove`.

## Common Failure Modes & Pitfalls

- Combining `--slug` with `--merged` let the selector loop fall through: it selected the named worktree and then every merged worktree. Ignored and untracked status (`!!` and `??`) did not block deletion; the incident removed gitignored QA artifacts.
- The incident removed gitignored QA artifacts from art-router. They were outside Git history; only a known backup could restore them.

## Environment Quirks & Tooling Gotchas

- Use `git status --porcelain=v1 --ignored=matching -z` to inspect tracked state plus ignored and untracked paths. Parse NUL-delimited records so unusual path characters do not confuse status detection.

## Learned Recovery Strategies

- Select exactly one cleanup mode. For a merged PR, use `python scripts/cli/harness.py clean --branch <full-branch> --pr <number>`; cleanup verifies PR state, base branch, PR head branch, and exact worktree HEAD before selecting one claim.
- Both the harness gate and direct worktree removal refuse untracked or ignored paths and report paths only. `--force` cannot override this guard. Move or back up the reported paths before retrying; if status cannot be inspected, preserve the worktree.

## Critical Success Factors

- Keep branch/PR cleanup exact and fail closed when claim, GitHub metadata, worktree branch, HEAD, or Git status cannot be verified.
- Use external backups as the recovery source for deleted ignored/untracked data; Git history only helps for tracked content.

# agent-factory

Public, product-agnostic agent factory. Any harness or router can invoke it with a [run spec](./docs/standards/run-spec.md): a QA fleet finds issues against a **declared target**, and an executive fleet turns accepted findings into pull requests toward a **declared promotion target**.

Eleven named agents and their skills live here. Callers pin a git ref of this repository and pass `AGENT.md` / `SKILL.md` paths plus the run spec. They do not need a second copy of the roster. Nothing in this tree hard-codes a product, employer system, host IDE, or calling harness.

Schedule cadence is unset; kickoffs are manual until an operator chooses one.

## Built on ai-harness-core

Scaffolded from [`Koality-Assured/ai-harness-core`](https://github.com/Koality-Assured/ai-harness-core). Pull allowlisted core updates with `python scripts/sync/pull_harness_core.py`. Propose generic harness changes back as issues via `python scripts/sync/propose_core_update.py` (never open a core PR from this tree). Factory agents, scenario packs, and the ledger stay here.

## Invoke from a harness

1. Checkout or pin this repo at a known ref.
2. Supply a complete run spec: `run_id`, `target`, `pack_id` or `pack_path`, `mode` (and optional `promotion_target` / `proof_mode`).
3. Spawn Mara (`qa-run`) or Adrian (`executive-triage`) with those paths and the run spec. Fail closed if required fields are missing.
4. Keep product-specific packs and live run records outside the public tree (see overlays below).

## Where to start

| Path | Role |
| --- | --- |
| [`AGENTS.md`](./AGENTS.md) | Agent operating rules |
| [`docs/standards/run-spec.md`](./docs/standards/run-spec.md) | Operator-intent invocation contract |
| [`docs/qa/scenario-packs/`](./docs/qa/) | Pack template + synthetic examples |
| [`docs/standards/finding-schema.md`](./docs/standards/finding-schema.md) | Finding record shape |
| [`ai-tooling/agents/`](./ai-tooling/agents/) | Factory roster (`mara`, `adrian`, …) |
| [`ai-tooling/skills/qa/`](./ai-tooling/skills/qa/) and [`executive/`](./ai-tooling/skills/executive/) | Factory skill families |
| [`.harness/domain.json`](./.harness/domain.json) | Spoke marker (public; domain `none`) |

## Private overlays

Product-specific scenario packs and absolute workstation paths MUST NOT ship as public defaults. Place them under `docs/qa/scenario-packs/overlays/` (gitignored) or outside this repository. Live ledgers, abuse evidence, and run locks under `results/qa/` are local-only (gitignored except `.gitkeep` placeholders).

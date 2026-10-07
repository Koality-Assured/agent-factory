# QA skills

Skills for factory QA personas: run orchestration, user simulation findings, ledger write-back, and the QA schedule stub.

## Rules

- Follow the shared skill contract in [`../skill-conventions.md`](../skill-conventions.md) and repository rules in [`../../AGENTS.md`](../../AGENTS.md).
- Findings MUST conform to [`../../../docs/standards/finding-schema.md`](../../../docs/standards/finding-schema.md). Findings without reproduction are invalid.
- `qa-schedule` cadence is deferred (**UNSET**) until a human sets it. Invocation is manual (first run is a manual kickoff). Do not invent an interval or arm cron.
- Owner agents are the factory first-name specialists under `ai-tooling/agents/<name>/`. Do not copy this roster into a calling harness; pin this repo and pass AGENT.md paths.

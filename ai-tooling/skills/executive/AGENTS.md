# Executive skills

Skills for factory executive promotion: ledger triage, deconflict, gated implementation, proof, security intent, pull-request path, merge validation, and the executive schedule stub.

## Rules

- Follow the shared skill contract in [`../skill-conventions.md`](../skill-conventions.md) and repository rules in [`../../AGENTS.md`](../../AGENTS.md).
- Consume only valid findings per [`../../../docs/standards/finding-schema.md`](../../../docs/standards/finding-schema.md).
- Honor [`../../../docs/standards/run-lock.md`](../../../docs/standards/run-lock.md): one executive batch at a time; no overlapping page edits.
- Promotion order is fixed: Adrian assigns → Julian deconflicts → Leo implements → Kenji proves → Nadia → Simone (PR only) → Julian validates → human merge. Nadia cannot be skipped. Simone alone opens the PR. Julian does not merge.
- `executive-schedule` cadence is deferred (**UNSET**) until a human sets it. Invocation is manual (first run is a manual kickoff). Do not invent an interval or arm cron.

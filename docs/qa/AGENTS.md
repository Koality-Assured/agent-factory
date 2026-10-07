# QA docs

Scenario packs and QA run contracts for this factory spoke.

## Rules

- Invocation uses the [run spec](../standards/run-spec.md). There is no default pack or product target.
- Scenario packs declare target assumptions in-file; use `_template.md` and synthetic `examples/` only in the public tree.
- Product packs live under `overlays/` (gitignored) or outside this repo.
- Findings conform to [`../standards/finding-schema.md`](../standards/finding-schema.md).
- Do not vendor calling-harness corpus into this tree — packs reference surfaces by run-spec target only.

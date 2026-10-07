---
doc_kind: process
canonical_id: scenario-pack-template
purpose: [process]
rank: high
topics: [qa, scenario-pack]
rag_keywords: [scenario-pack, template, operator-intent, run-spec, read-only]
---

# Scenario pack template

Copy this file when authoring a pack. Replace every placeholder. Do not hard-code a product or workstation path into factory skills — pass the pack via the [run spec](../../standards/run-spec.md).

## Assumption (proceed)

**Target:** `<describe the surface under test; use $TARGET_CHECKOUT or a run-spec target string>`

Findings MUST conform to [`docs/standards/finding-schema.md`](../../standards/finding-schema.md).

## Run inputs

| Field | Value |
| --- | --- |
| `target` | From run spec (required) |
| `mode` | `read-only` (typical) |
| `pack_id` | `<kebab-case-pack-id>` |

## Cadence / kickoff

Cadence is **UNSET** unless the operator sets one. Do not invent an interval.

## Persona briefs

| Persona | Focus |
| --- | --- |
| Priya | Follow the obvious path through the target. |
| Elena | Correct / advanced use. Class overbuilt ideas as `power-user-preference`. |
| Owen | Get lost; try actions that should fail. Cap **five** findings. |
| Marcus | Misuse **inside the declared target only**. No production credentials. No write tools. |

Optional pack-selected personas (for example accessibility) may be listed here when their `AGENT.md` exists; they are not always-on.

## Out of scope

- Editing the target or this factory during the QA run.
- Arming cron without an operator-set cadence.
- Executive promotion (Adrian path).
- Targets outside the run-spec `target`.

## Success

Mara records deduped schema-valid findings with reproduction. No target edits. Pack remains an operator-supplied input.

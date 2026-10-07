---
doc_kind: process
canonical_id: scenario-pack-example-web-app
purpose: [process]
rank: medium
topics: [qa, scenario-pack, example]
rag_keywords: [scenario-pack, example-web-app, synthetic, read-only]
---

# Scenario pack example: synthetic web app

Synthetic public example. Not a default. Operator MUST still pass `target` and `pack_id` / `pack_path` in the [run spec](../../../standards/run-spec.md).

## Assumption (proceed)

**Target:** a local checkout of a small HTML/CSS/JS app at `$TARGET_CHECKOUT` (never a hard-coded workstation path).

## Run inputs

| Field | Value |
| --- | --- |
| `target` | `$TARGET_CHECKOUT` (from run spec) |
| `mode` | `read-only` |
| `pack_id` | `example-web-app` |

## Cadence / kickoff

Cadence **UNSET**. Manual kickoff only.

## Persona briefs

| Persona | Focus |
| --- | --- |
| Priya | Open the app, follow the primary navigation and happy path. |
| Elena | Exercise secondary flows (settings, import/export, edge states) without inventing out-of-app tooling. |
| Owen | Click the wrong controls, ignore prompts, try actions that should fail. Cap **five** findings. |
| Marcus | Probe in-app state assumptions and UI-exposed write paths **inside the checkout only**. No production credentials. |

## Out of scope

- Editing `$TARGET_CHECKOUT` or this factory during the QA run.
- Product-specific packs (those live in private overlays).

## Success

Schema-valid findings with reproduction against the operator-supplied target.

---
doc_kind: standard
canonical_id: factory-run-spec
purpose: [standard, requirement]
rank: high
topics: [agents, qa, run-spec]
rag_keywords: [run-spec, operator-intent, target, scenario-pack, pack_id, promotion-target, objective, opportunity-discovery, product-agnostic]
---

# Factory run spec (operator intent)

Normative contract for invoking the agent factory. The review target and scenario pack come from **operator intent at invocation**. Skills and agents MUST NOT assume a product, host path, or host IDE.

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `run_id` | string | Correlation id for the ledger and private run record. |
| `target` | string | System under test: checkout path, URL, or repo ref. Never implied. |
| `pack_id` or `pack_path` | string | Scenario pack selected for this run. Exactly one MUST be provided. |
| `mode` | string | Persona mode for the QA sweep (typically `read-only`). |

## Optional fields

| Field | Type | Description |
| --- | --- | --- |
| `promotion_target` | string | Repo or surface that receives executive pull requests. |
| `proof_mode` | string | How Kenji proves claims: `local-replay`, `staging`, or as declared. |
| `staging_host` | string | Staging URL when `proof_mode` is `staging`. |
| `host_tool` | string | Metadata only (Cursor, Claude Code, …). MUST NOT change agent contracts. |
| `objective` | string | `problems`, `opportunities`, or `both`. Omission means `problems` for compatibility with existing run specs. |

## QA objective

`objective` selects the QA work:

- `problems`: preserve the existing defect and abuse sweep.
- `opportunities`: look for evidenced unmet workflows, capability gaps, and meaningful workarounds. Dispatch Owen, Priya, and Elena; do not dispatch Marcus's abuse-only pass.
- `both`: run the existing defect and abuse sweep and the opportunity-discovery pass. Keep defect, abuse, and opportunity findings distinct.

Every emitted finding records the selected objective. A finding with no objective in a historical run is interpreted as `problems`. Objective selection changes QA focus only; it does not change target, access mode, security limits, or promotion controls.

## Fail closed

- Missing `run_id`, `target`, or pack (`pack_id` / `pack_path`) → refuse the run.
- Missing staging host when `proof_mode` is `staging` → refuse inventing a host; use `local-replay` only when the run spec says so.
- Product-specific packs (real product names, private paths) MUST NOT be the public default. Ship them as operator overlays under `docs/qa/scenario-packs/overlays/` (gitignored) or outside this repo.

## Scenario packs

Packs are libraries of persona briefs. See [`docs/qa/scenario-packs/_template.md`](../qa/scenario-packs/_template.md). Synthetic examples may live under `examples/`. There is **no default pack**.

## Serialization

JSON object keys use snake_case. Example (illustrative):

```json
{
  "run_id": "run-001",
  "target": "$TARGET_CHECKOUT",
  "pack_id": "example-web-app",
  "mode": "read-only",
  "promotion_target": "example-org/example-app",
  "proof_mode": "local-replay",
  "objective": "both"
}
```

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
| `tier` | string | Execution tier: `direct` or `full-assurance` (default `full-assurance`). |
| `git_trailers` | boolean | Whether to append git provenance trailers to commits (default `true`). |
| `promotion_target` | string | Repo or surface that receives executive pull requests. |
| `proof_mode` | string | How Kenji proves claims: `local-replay`, `staging`, or as declared. |
| `staging_host` | string | Staging URL when `proof_mode` is `staging`. |
| `host_tool` | string | Metadata only (Cursor, Claude Code, …). MUST NOT change agent contracts. |
| `objective` | string | `problems`, `opportunities`, or `both`. Omission means `problems` for compatibility with existing run specs. |

## Execution tiers

Run specs declare an explicit `tier` parameter to govern pipeline overhead:

- **`direct`**: Designed for localized, single-worktree defect fixes with existing automated tests or clear deterministic reproductions. Bypasses redundant multi-agent deconfliction and triage while strictly preserving the separation of implementation, proof, and review.
  - **Pipeline Flow**: Leo (implement) -> Kenji (replay suite & head-bound proof) -> Simone (finding adjudication & PR authoring).
  - **Latency & Cost**: Minimal token overhead, fast turnaround, high test-backed confidence.
- **`full-assurance`**: The complete 11-agent multi-stage discovery, triage, deconfliction, proof, security review, finding adjudication, and promotion pipeline.
  - **Pipeline Flow**: Mara & QA Fleet -> Adrian -> Julian -> Leo -> Kenji -> Nadia -> Simone -> Julian -> Human Merge.
  - **When Required**: Broad exploratory QA, multi-file architectural changes, cross-module refactors, new feature additions, or security boundary modifications.

## Negative routing criteria ("Not a reason to escalate")

To prevent LLM coordinators from defaulting to `full-assurance` for routine tasks (which causes massive context bloat and token exhaustion), coordinators MUST consult the negative routing criteria:

| Scenario | Coordinator Temptation | Prescribed Tier | Enforced Rationale |
| :--- | :--- | :--- | :--- |
| Scoped bugfix with existing failing test | "Escalate to full-assurance to ensure system-wide safety" | `direct` | The failure mode and regression boundary are already codified in tests. Kenji's head-bound cryptographic proof validates the fix without multi-agent triage. |
| Pure documentation, markdown, or typo correction | "Escalate to run Nadia security architect review" | `direct` | Documentation edits touch no runtime code, API contracts, or privilege boundaries. Full assurance wastes token budget and adds friction. |
| Standard dependency update within semver range | "Escalate for Marcus adversarial abuse sweep" | `direct` | Package managers and existing test replay catch regressions without full fuzzing or abuse analysis. |
| Scoped refactor bounded to single isolated worktree | "Escalate to Julian deconfliction and Adrian triage" | `direct` | The task operates entirely within an isolated worktree with no branch collision risk; multi-agent deconfliction is redundant. |

## Standardized Git provenance trailers

All commits authored by factory developers (Leo, Simone) and promoted to target repositories MUST append standardized git trailers to their commit messages when `git_trailers` is true:

```gitcommit
Co-Authored-By: Agent Factory <agent-factory@local>
X-Factory-Run: <run_id>
X-Factory-Ledger-ID: <finding_id>
```

- **`Co-Authored-By`**: Standard attribution recognizing the Agent Factory automation identity (`Agent Factory <agent-factory@local>`).
- **`X-Factory-Run`**: Exact `run_id` matching historical records in `agent-factory-history-archive/results/qa/runs/<run_id>/`.
- **`X-Factory-Ledger-ID`**: Finding ID from the deduplicated ledger (`results/qa/ledger/<run_id>.json`).

This establishes a permanent, bidirectional audit trail connecting any production commit in the target repository directly to its underlying QA discovery, Kenji SRE proof receipt, and Simone adjudication ledger in the cold archive.

## Cross-model diversity

To prevent shared blind spots, model hallucinations, and common failure modes from leaking into production, factory runs mandate cross-model diversity between author and reviewer:
- The implementer (**Leo**) runs on the primary model family (e.g. Gemini 3.8 Flash / Flash-High).
- Reviewers and auditors (**Nadia**, **Simone**, or adversarial sub-passes) run on a distinct secondary model family (e.g. Claude 3.7 / 3.5 Sonnet per secondary allocation rules).

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
  "tier": "direct",
  "git_trailers": true,
  "promotion_target": "example-org/example-app",
  "proof_mode": "local-replay",
  "objective": "both"
}
```

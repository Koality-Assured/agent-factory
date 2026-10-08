---
doc_kind: standard
canonical_id: finding-schema
purpose: [standard, requirement]
rank: high
topics: [agents, qa, findings]
rag_keywords: [finding, ledger, reproduction, defect, opportunity, abuse, persona, evidence, triage-status]
---

# Finding schema

Normative contract for QA and executive ledger findings in this factory spoke. Skills that record or consume findings MUST conform. A finding must include a reproducible observation; an opportunity must also include concrete evidence, user impact, and testable success criteria.

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Stable unique id for the finding within a run or ledger. |
| `persona` | string | Persona that produced the finding (agent first name or role id). |
| `target` | string | Declared target under test (product surface, host, or run-spec target). |
| `objective` | enum | `problems`, `opportunities`, or `both`, copied from the run spec. Historical findings without it default to `problems`. |
| `what_they_tried` | string | What the persona attempted. |
| `reproduction` | string | Concrete steps another agent can follow to reproduce the observed behavior or task/workaround. Required; empty or missing makes the finding invalid. |
| `expected_result` | string | For defects, what should have happened. For opportunities, the useful outcome the user is trying to achieve. |
| `actual_result` | string | For defects, what happened instead. For opportunities, the current capability limit or friction observed. |
| `class` | enum | New findings use exactly one of: `defect`, `opportunity`, `abuse`. |
| `evidence` | string[] | Required for `opportunity`: concrete target observations or sources, with paths, locations, or reproducible actions where available. |
| `impact` | string | Required for `opportunity`: affected users/workflows and the observed consequence or cost. Separate observed facts from estimates. |
| `success_criteria` | string[] | Required for `opportunity`: observable, testable outcomes that would address the unmet need without prescribing an implementation. |

## Validity

- A finding is **valid** only when every common field is present and non-empty, and `reproduction` contains actionable steps.
- A finding without `reproduction` is **invalid** and MUST NOT enter the ledger.
- An `opportunity` is valid only when `evidence`, `impact`, and `success_criteria` are each present and specific enough to verify. Ideas based only on taste, hypothetical users, or unsupported feature requests MUST be omitted.
- In a `problems` run, emit only defect or abuse findings. In an `opportunities` run, emit only opportunity findings. In a `both` run, classify each finding separately and do not turn a preference into a defect.
- `class` MUST be one of the three new-output enum values above; other new labels are refused.

## Ledger triage state

QA adds valid findings to the ledger with `triage_status: open`. Historical ledger entries with no `triage_status` are also treated as open. This means the item is ready for automatic executive triage; it does not mean a human must accept it. Adrian evaluates every open and previously deferred item, including opportunities, and assigns a priority (`P0` through `P3`). Julian marks selected items `assigned` after recording their deconflicted work items. Lower-priority items may be marked `deferred` with a reason and remain eligible for a later executive batch. Unsupported or duplicate legacy entries may be marked `rejected` with a reason. After the promotion path and human merge, mark the item `closed`.

Allowed `triage_status` values are `open`, `assigned`, `deferred`, `rejected`, and `closed`. `priority` is set by Adrian during triage: `P0` for an urgent safety, security, data-loss, or service-wide failure; `P1` for a severe or broadly blocking workflow; `P2` for a material but bounded workflow gap; `P3` for a lower-impact improvement. Use observed reach, impact, urgency, and evidence quality to choose. Every valid item moved to `assigned` or `deferred` receives a priority. A `reason` is required when an item is `deferred` or `rejected`. There is no `pending-human-acceptance` state.

Historical ledger entries labeled `power-user-preference` remain readable for migration only. Adrian must reclassify one as an `opportunity` only when its evidence, impact, and success criteria meet this contract; otherwise reject it with a reason. New QA runs must not emit `power-user-preference`.

## Serialization

JSON object keys use snake_case as in the table. Example (illustrative; not a live finding):

```json
{
  "id": "run-001-f-03",
  "persona": "priya",
  "target": "$TARGET_CHECKOUT",
  "objective": "problems",
  "what_they_tried": "Followed the documented path to create a page.",
  "reproduction": "1. Open the target. 2. Click New page. 3. Submit with title only.",
  "expected_result": "Page is created and listed.",
  "actual_result": "Form returns a validation error with no field highlighted.",
  "class": "defect",
  "triage_status": "open"
}
```

Opportunity example (illustrative; not a live finding):

```json
{
  "id": "run-002-f-01",
  "persona": "elena",
  "target": "$TARGET_CHECKOUT",
  "objective": "opportunities",
  "what_they_tried": "Tried to export a multi-page report while preserving its structure.",
  "reproduction": "1. Create a three-page report. 2. Use the available export options. 3. Inspect the exported result.",
  "expected_result": "The report can be exported as an editable document with its page structure intact.",
  "actual_result": "Available exports flatten the report; the only observed workaround is manual reconstruction.",
  "class": "opportunity",
  "evidence": ["Export menu exposes PDF and image only.", "Reproduced flattening on a three-page report; target path: export flow."],
  "impact": "Users who need to revise or reuse multi-page reports must rebuild the structure by hand; this affects the tested report workflow.",
  "success_criteria": ["A three-page report exports to an editable format.", "Page order and headings remain intact after export."],
  "triage_status": "open"
}
```

## Ownership

This spoke owns the finding contract. Do not propose this file back to `ai-harness-core`. Live run records stay private in this factory; promotion-safe controls are decided later by the executive path.

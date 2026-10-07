---
doc_kind: standard
canonical_id: finding-schema
purpose: [standard, requirement]
rank: high
topics: [agents, qa, findings]
rag_keywords: [finding, ledger, reproduction, defect, power-user-preference, abuse, persona]
---

# Finding schema

Normative contract for QA and executive ledger findings in this factory spoke. Skills that record or consume findings MUST conform. Findings without reproduction are invalid and MUST be dropped.

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Stable unique id for the finding within a run or ledger. |
| `persona` | string | Persona that produced the finding (agent first name or role id). |
| `target` | string | Declared target under test (product surface, host, or run-spec target). |
| `what_they_tried` | string | What the persona attempted. |
| `reproduction` | string | Concrete steps another agent can follow to reproduce. Required; empty or missing makes the finding invalid. |
| `expected_result` | string | What should have happened. |
| `actual_result` | string | What happened instead. |
| `class` | enum | Exactly one of: `defect`, `power-user-preference`, `abuse`. |

## Validity

- A finding is **valid** only when every required field is present and non-empty, and `reproduction` contains actionable steps.
- A finding without `reproduction` is **invalid** and MUST NOT enter the ledger.
- `class` MUST be one of the three enum values above; other labels are refused.

## Serialization

JSON object keys use snake_case as in the table. Example (illustrative; not a live finding):

```json
{
  "id": "run-001-f-03",
  "persona": "priya",
  "target": "$TARGET_CHECKOUT",
  "what_they_tried": "Followed the documented path to create a page.",
  "reproduction": "1. Open the target. 2. Click New page. 3. Submit with title only.",
  "expected_result": "Page is created and listed.",
  "actual_result": "Form returns a validation error with no field highlighted.",
  "class": "defect"
}
```

## Ownership

This spoke owns the finding contract. Do not propose this file back to `ai-harness-core`. Live run records stay private in this factory; promotion-safe controls are decided later by the executive path.

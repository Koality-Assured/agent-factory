---
doc_kind: standard
canonical_id: run-lock
purpose: [standard, requirement]
rank: high
topics: [agents, executive, qa, concurrency]
rag_keywords: [run-lock, executive-batch, page-overlap, ledger, concurrency]
---

# Run lock

Normative concurrency contract for factory executive batches. Executive skills MUST read this before assigning work.

## Rules

1. **One executive batch at a time.** Only one Adrian `executive-triage` batch may hold the lock.
2. **No overlapping page edits.** Two runs (QA or executive) MUST NOT claim the same promotion-target paths for mutation. Executive claims are exclusive for the pages in the batch.
3. **Lock file.** Record lock state under `results/qa/run-lock.json` (or successor path named by the executive skill) with: `holder`, `batch_id`, `claimed_pages`, `acquired_at`, `status` (`held` | `released`).
4. **Acquire before assign.** Adrian MUST acquire the lock before spawning Leo. If the lock is held or claimed pages intersect, stop and surface to a human.
5. **Release after batch.** Release when the batch completes, fails, or a human aborts. Do not leave a stale hold without recording the failure.
6. **QA vs executive.** Mara's QA runs are read-only against the promotion target and do not take the executive lock, but MUST NOT schedule promotion-target mutations. Executive mutations honor this lock.

## Non-goals

- Not a host cron or scheduler.
- Not a substitute for git branch isolation (`isolate-work`).
- Not authorization against malicious actors — cooperative coordination only.

## Ownership

This spoke owns the run-lock contract. Do not propose this file back to `ai-harness-core`.

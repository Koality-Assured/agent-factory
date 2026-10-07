# Standalone agents

Human overview: specialist definitions live in `<id>/AGENT.md`. Optional host stubs under `.cursor/agents/` only point here.

**Agents do not use this README as a catalog.** Catalogs are `AGENT.md` (Schema V2) + [`../../routing/skill-dispatch.md`](../../routing/skill-dispatch.md) / [`../../routing/area-map.md`](../../routing/area-map.md). Tiers: [`model-tiers.md`](./model-tiers.md).

Human index (not agent SoT):

### Broad-sweeping operators

| Operator | Role / Scope | Tier |
| --- | --- | --- |
| [`harness-operator/`](./harness-operator/) | Harness lifecycle, control plane, cost layers, skill/agent builder, repository maintenance | standard |
| [`document-operator/`](./document-operator/) | Technical writing, diagrams, reports, Confluence/Slack/Google collab, anti-slop | standard |
| [`research-operator/`](./research-operator/) | Deep technical research, BenchLM, AI vendor tracking, community intelligence, web crawl | high |
| [`security-tooling-operator/`](./security-tooling-operator/) | Defensive assessments, threat modeling, AD/Windows audit, network discovery, packet review | standard |

### Coordinator & true specialists

| Specialist | Role | Tier |
| --- | --- | --- |
| [`router/`](./router/) | Parent coordinator: classify, isolate, spawn | standard |
| [`as-code-agent/`](./as-code-agent/) | Dedicated Terraform/OpenTofu/IaC authoring & plan validation | high |
| [`detailed-activity/`](./detailed-activity/) | Dedicated adversarial / antagonistic review and challenge audits | high |
| [`benchmark-agent/`](./benchmark-agent/) | Empirical benchmarking: cost estimation, fleet dry runs, retrieval, tool efficiency | standard |
| [`github-ops/`](./github-ops/) | GitHub PR workflow, branch discipline, issue management | standard |
| [`git-fast-operator/`](./git-fast-operator/) | Simple git fetch/status/log/diff/sync | fast |


### Factory spoke specialists

These eleven are owned by this factory spoke only. Do not copy this roster into a calling harness; pin this repo and pass AGENT.md paths.

| Specialist | Role | Tier |
| --- | --- | --- |
| [`mara/`](./mara/) | QA leader: start run, dispatch personas, dedupe findings | standard |
| [`owen/`](./owen/) | Incompetent user persona (findings only; cap five) | fast |
| [`priya/`](./priya/) | Regular user persona (findings only) | fast |
| [`elena/`](./elena/) | Competent user persona (findings only) | standard |
| [`marcus/`](./marcus/) | Abuse tester persona (private evidence) | standard |
| [`adrian/`](./adrian/) | Executive: assign work; does not implement | high |
| [`julian/`](./julian/) | Project coordinator: deconflict before Leo; validate after Simone PR | high |
| [`leo/`](./leo/) | Standard developer: implement in isolated worktree | standard |
| [`kenji/`](./kenji/) | SRE: prove change (staging or local replay per run spec) | standard |
| [`nadia/`](./nadia/) | Security architect: required intent/security gate | high |
| [`simone/`](./simone/) | Senior developer: review; only agent who opens PR | high |

### Legacy & component specialists (Consolidated into Operators)

| Agent | Consolidated into | Tier |
| --- | --- | --- |
| [`documentation-ops/`](./documentation-ops/) | `document-operator` | standard |
| [`router-maintenance/`](./router-maintenance/) | `harness-operator` | standard |
| [`qmd-ops/`](./qmd-ops/) | `harness-operator` | standard |
| [`ai-tooling-ops/`](./ai-tooling-ops/) | `harness-operator` | standard |
| [`memory-operator/`](./memory-operator/) | `harness-operator` | standard |
| [`script-ops/`](./script-ops/) | `harness-operator` | standard |
| [`artifact-agent/`](./artifact-agent/) | `document-operator` | standard |
| [`reference-ops/`](./reference-ops/) | `document-operator` | standard |
| [`repo-sync-ops/`](./repo-sync-ops/) | `harness-operator` | standard |

A2A specifications & schemas: canonical in `AGENT.md` (Schema V2); see also [`../a2a/agent-cards/README.md`](../a2a/agent-cards/README.md).

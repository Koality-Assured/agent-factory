---
doc_kind: reinforcement
canonical_id: naming-conventions
purpose: [reinforcement]
rank: high
topics: [agents, naming]
rag_keywords:
  [
    Agent Factory,
    The Factory,
    factory,
    project-name,
  ]
---

# Project naming conventions

## Project-as-a-whole names

Project-as-a-whole names all mean this repository. Pick any of them when you mean this repo; they name the same project, not several products.

- Agent Factory
- The Factory
- factory (spoken shorthand)

## What is not a project name

These labels are a folder, an activity, an agent, or the git slug. They are not spoken names for the project as a whole.

- `routing/` — the generated next-step index folder after root AGENTS.md
- "routing" — the activity of matching skill-dispatch / area-map
- `router` — the specialist agent under `ai-tooling/agents/router/`
- `agent-factory` — the git/repo slug only; not a spoken project name
- A calling harness or domain router — those are separate repositories that *invoke* this factory; they are not this project

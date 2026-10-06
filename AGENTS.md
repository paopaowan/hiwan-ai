# AGENTS.md

> Hiwan AI OS — AI-facing project entry point
>
> Version: 1.0
> Status: Active
> Last reviewed: 2026-10-06

## 1. Mission

Hiwan AI OS is a local-first personal and family AI operating system.

The project aims to evolve from a personal AI assistant into a trustworthy, modular family agent platform while keeping long-lived data, identity, permissions, memory, models, and tools independently replaceable.

## 2. Owner and working relationship

- Owner: Richard
- The primary human decision-maker is Richard.
- AI assistants are consultants and implementation partners, not final authorities.
- Important architectural decisions should be explainable, reviewable, and recorded.

## 3. Core principles

1. **Local-first** — private and durable data should remain local whenever practical.
2. **Agent != Model** — agents must not be tightly coupled to a particular model.
3. **Agent != Memory** — long-lived memory belongs to a separate data/knowledge layer.
4. **Agent != Data** — agents access data through explicit tools and policies.
5. **Identity → Policy → Tool → Data** — access should follow this order.
6. **Composable OSS first** — prefer proven open-source components over unnecessary reinvention.
7. **Avoid premature framework lock-in** — do not adopt a large agent framework until a concrete requirement justifies it.
8. **Human approval for high-impact actions** — especially financial, external, destructive, or family-sensitive actions.
9. **Knowledge should outlive models** — Markdown, databases, files, and other durable knowledge must remain usable when models or runtimes change.
10. **Evidence over assumption** — distinguish verified facts, design decisions, hypotheses, and open questions.

## 4. Current architecture direction

```text
hiwan.ai
   ↓
API Gateway
   ↓
Agent Runtime
   ├── Personal Agent
   ├── Family Agent
   ├── Language Agent
   ├── Education Agent
   ├── Finance Agent
   ├── Research Agent
   └── Coding Agent
   ↓
MCP / Tools
   ↓
Memory / Data Layer
   ├── PostgreSQL
   ├── Search / vector layer (later, when justified)
   ├── Object / file storage
   └── Markdown knowledge
   ↓
Local-first infrastructure
```

This is a direction, not a claim that every component already exists.

## 5. Current state

As of 2026-10-06:

- Git and GitHub repository are established.
- Python 3.13 + uv + project virtual environment are established.
- Node.js/npm are installed.
- Docker/Compose are installed and verified.
- Obsidian is installed for human-facing Markdown knowledge work.
- Ollama is installed and verified.
- The first local model is being downloaded/validated.
- No large agent framework has been adopted yet.
- PostgreSQL, vector search, Open WebUI, LangChain, CrewAI, and similar components remain intentionally unselected unless a concrete requirement appears.

## 6. How an AI should work in this repository

Before proposing architecture:

1. Read this file.
2. Read `AI_CONTEXT.md`.
3. Inspect relevant files under `architecture/`, `agents/`, `memory/`, `mcp/`, `knowledge/`, and `learning/`.
4. Read `DECISIONS.md` before contradicting or replacing an established decision.
5. Treat `learning/` as engineering evidence, including failures and gotchas.
6. Separate:
   - verified facts
   - current decisions
   - assumptions
   - proposals
   - unresolved questions
7. Prefer the smallest reversible change that moves the project forward.
8. When challenging the architecture, explain the trade-off and provide an alternative.

## 7. Do not

- Invent project history.
- Treat a proposal as an implemented component.
- Introduce dependencies merely because they are popular.
- Store sensitive personal/family data in source code or public repositories.
- Replace an established decision silently.
- Optimize for framework features before the underlying requirement is clear.

## 8. Decision protocol

For meaningful architectural changes, produce:

- Problem
- Current state
- Options considered
- Trade-offs
- Recommendation
- Reversibility / migration impact
- Security/privacy impact
- Decision owner

Record accepted decisions in `DECISIONS.md`.

## 9. Review and maintenance

This file is intentionally short and stable.

Update it only when a principle, project-wide workflow, or durable architectural invariant changes.

Do not put daily progress or detailed history here. Put those in `AI_CONTEXT.md`, `learning/`, architecture documents, or Git history.

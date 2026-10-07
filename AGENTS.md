# AGENTS.md

## Mission

Hiwan AI OS is a long-term local-first personal and family AI system.

The project aims to preserve user-owned knowledge, memory, learning history, projects, and future family capabilities independently from any specific AI model or agent framework.

Richard is the project owner and final human decision-maker.

## Core Principles

1. Local-first for personal and family data.
2. Agent != Model.
3. Agent != Memory.
4. Agent != Data.
5. Model != Runtime.
6. Identity -> Policy -> Tool -> Data.
7. Knowledge should outlive individual models and frameworks.
8. Prefer OSS and portable interfaces.
9. Avoid premature framework lock-in.
10. Human approval is required for high-impact actions.
11. Evidence is preferred over assumption.
12. Architecture changes should be independently reviewable.

## Core Boundaries

Hiwan AI separates the following concerns:

```text
Model
  !=
Runtime
  !=
Agent
  !=
Tool
  !=
Memory
  !=
Data
  !=
Identity
  !=
Policy
```

These boundaries are architectural goals and should be preserved unless a documented decision explicitly changes them.

## Public Software / Private Data

Hiwan AI uses a deliberate public-software / private-data boundary.

### Public repository

The repository may contain:

- source code
- architecture
- technical documentation
- AI context
- architecture proposals and reviews
- non-sensitive learning notes
- tests
- configuration templates
- infrastructure definitions that contain no secrets
- OSS integration code and documentation

### Private/local data

Private personal and family information must remain outside the public repository, including:

- personal memory
- family memory
- conversations
- private documents
- financial information
- credentials and secrets
- API keys and tokens
- private photos/media
- local databases
- private vector indexes
- local model/runtime data

Public architecture and software are expected.

Private personal/family data is not.

## Public Repository Boundary

Assume this repository is intended to be public.

AI agents must therefore:

- never commit secrets, credentials, API keys, tokens, or private keys
- never commit personal or family data
- never introduce real private documents into examples or tests
- use synthetic/example data when demonstrating personal or family workflows
- treat local memory and data stores as outside the public repository
- flag any proposed change that could expose private data through source control

Public architecture and software are expected.
Private personal/family data is not.

## Local-First Data Tiers

The current direction is:

### L0 — Local Only

Highly sensitive information:

- family data
- private conversations
- credentials
- sensitive personal records
- private documents

### L1 — Local + Encrypted Backup

User-owned durable knowledge:

- learning
- project knowledge
- documentation
- non-sensitive personal knowledge
- structured knowledge

### L2 — Cloud Allowed

Non-sensitive workloads:

- public research
- coding assistance
- public website content
- cloud inference when appropriate
- public web search

The exact implementation is still subject to future architecture decisions.

## Current Architecture Direction

```text
hiwan.ai
    |
    v
API Gateway
    |
    v
Agent Runtime
    |
    +--> Identity / Policy
    |
    +--> MCP / Tools
    |
    +--> Memory / Data
```

The current architecture is intentionally incomplete.

Do not assume that planned components are already implemented.

## Current Runtime Direction

Ollama is the initial local AI runtime.

The first model baseline is currently Qwen3.5 27B MLX on Apple Silicon.

This is an experimental runtime/model choice and should not be treated as a permanent architectural commitment.

## Durable Knowledge

Markdown is the current durable knowledge format.

The intended human-facing workflow is:

```text
Obsidian
   |
   v
Markdown
   |
   v
Git
   |
   v
Knowledge Layer
   |
   v
Search / Retrieval
   |
   v
Agents / hiwan.ai
```

Do not introduce a database or vector store merely because it is popular.

Introduce structured storage when a demonstrated requirement justifies it.

## Architecture Governance

Meaningful architecture changes follow:

```text
Proposal
   |
   v
Independent Review
   |
   v
Richard Decision
   |
   v
DECISIONS.md
   |
   v
Implementation
   |
   v
Learning / Post-Implementation Review
```

Proposal != Review != Decision.

An AI reviewer must not silently turn a proposal into an accepted decision.

## Evidence Labels

When reasoning about the project, distinguish:

- FACT — verified current state
- DECISION — explicitly accepted project decision
- PROPOSAL — suggested future change
- ASSUMPTION — unverified belief
- OPEN — unresolved question

Do not present assumptions or proposals as facts.

## AI Working Rules

Before making meaningful architecture recommendations, read:

1. `AGENTS.md`
2. `AI_CONTEXT.md`
3. `ARCHITECTURE.md`
4. `DECISIONS.md`
5. `ROADMAP.md`
6. relevant files under `architecture/`
7. relevant learning notes when historical context matters
8. `skills/hiwan-ai-review/SKILL.md` when performing architecture review

Do not invent project history.

Do not claim that an unimplemented feature exists.

Do not introduce dependencies merely because they are popular.

Do not silently replace an existing accepted decision.

When a proposal conflicts with an accepted decision, explicitly identify the conflict.

## Family Agent Safety

Future family-agent capabilities must be identity-aware and permission-aware.

Agents should never receive unrestricted access to personal or family data.

High-impact actions should require explicit policy checks and, where appropriate, human approval.

Examples include:

- financial actions
- external communication
- account changes
- destructive operations
- sensitive data sharing

## Maintainability

Keep project context concise and stable.

Use:

- `AGENTS.md` for AI operating rules
- `AI_CONTEXT.md` for broader project context
- `ARCHITECTURE.md` for current architecture
- `DECISIONS.md` for accepted decisions
- `ROADMAP.md` for planned work
- `architecture/` for proposals, reviews, and evidence
- `learning/` for chronological learning history

Do not turn `AGENTS.md` into a daily journal.

## Final Authority

Richard remains the final decision-maker.

No model, framework, reviewer, or automated process has authority to approve an architecture decision on behalf of the project owner.

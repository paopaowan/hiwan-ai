# Architecture Decisions

This document records accepted project decisions.

A proposal or review is not an accepted decision until Richard explicitly accepts it.

## Decision 001 — Local-First Architecture

**Status:** ACCEPTED

Hiwan AI will prioritize local-first operation for personal and family data.

Sensitive user-owned data should remain under local control whenever practical.

Cloud services may be used for non-sensitive workloads or where cloud processing provides clear value and is explicitly permitted.

## Decision 002 — Separate Agent, Model, Memory, and Data

**Status:** ACCEPTED

Agents, models, memory, and durable data are separate architectural concerns.

No single agent framework or model should become the owner of durable user knowledge.

## Decision 003 — Identity -> Policy -> Tool -> Data

**Status:** ACCEPTED

Access to personal and family data should follow:

```text
Identity
   ->
Policy
   ->
Tool
   ->
Data
```

Agents should not receive unrestricted access to private data.

This boundary is important for future family-agent functionality.

## Decision 004 — Markdown as Durable Knowledge Format

**Status:** ACCEPTED

Markdown is the initial durable knowledge format.

The goal is portability, human readability, Git compatibility, and independence from a specific AI framework.

## Decision 005 — Python 3.13 and uv

**Status:** ACCEPTED

Python 3.13 and uv are the initial Python development environment.

## Decision 006 — Ollama as Initial Local AI Runtime

**Status:** ACCEPTED

Ollama is the initial local AI runtime for Hiwan AI.

This is a runtime choice, not a permanent model commitment.

## Decision 007 — Avoid Premature Agent Framework Lock-In

**Status:** ACCEPTED

Hiwan AI will not adopt a large agent framework merely because it is popular.

The project should first understand the minimum agent loop and only introduce abstractions justified by demonstrated requirements.

## Decision 008 — Multi-AI Independent Architecture Review

**Status:** ACCEPTED

Important architecture changes should be independently reviewable by multiple AI systems when practical.

GPT, Gemini, Claude, and other reviewers may provide independent technical opinions.

The final decision remains with Richard.

## Decision 009 — Learning Includes Failures and Gotchas

**Status:** ACCEPTED

The learning journal should record:

- successful work
- failures
- debugging lessons
- gotchas
- architectural decisions
- open questions
- commands and operational knowledge

Failed approaches are part of the project's engineering knowledge.

## Decision 010 — Public Software / Private Data Boundary

**Status:** ACCEPTED

Hiwan AI will use a **Public Software / Private Data** architecture boundary.

### Public repository

The GitHub repository may contain:

- source code
- architecture
- technical documentation
- AI context and review protocols
- non-sensitive learning notes
- configuration templates
- tests
- infrastructure definitions that contain no secrets
- OSS integration code and documentation

### Private/local data

Personal and family data must remain outside the public repository, including:

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

### Architectural principle

The repository is the **software and architecture layer**.

Local storage is the **personal/family data layer**.

Therefore:

**Public software does not imply public data.**

Agents must access private data through explicit identity, policy, and tool boundaries rather than through Git repository access.

### Consequences

1. `hiwan-ai` may be a public GitHub repository.
2. Personal/family data must never be committed to the repository.
3. `.gitignore` must protect common local/private data locations.
4. Secrets must never be stored in source control.
5. Public-readiness checks should be performed before exposing the repository.
6. Architecture and implementation can be independently reviewed by GPT, Gemini, Claude, and other AI systems.
7. Any future requirement to store sensitive information in GitHub requires a new architecture/security decision.

### Rationale

Hiwan AI is intended to benefit from open architecture, OSS collaboration, and independent AI review while keeping user-owned personal and family data local-first and private.

This decision reinforces:

```text
Agent != Model != Memory != Data
```

and:

```text
Identity -> Policy -> Tool -> Data
```

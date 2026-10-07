# Hiwan AI OS Architecture

## Status

Current architecture direction.

This document describes the current system shape, not every future implementation detail.

Architecture changes should be evaluated through the proposal/review/decision process.

## North Star

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

The long-term goal is a local-first personal AI system that can evolve into a family AI system while keeping user-owned data portable and independent from any particular model or agent framework.

## Core Architectural Boundaries

The system deliberately separates:

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

### Model

A model performs inference.

Examples may include local or cloud LLMs.

A model should not own durable user knowledge.

### Runtime

A runtime hosts and serves models.

The first local runtime is Ollama.

### Agent

An agent is application-level behavior and orchestration.

An agent should not be treated as the storage system for user memory.

### Tool

A tool provides a bounded capability.

Examples include filesystem operations, web access, APIs, and future MCP tools.

### Memory

Memory represents information useful to agents over time.

Memory storage must remain independent from any single agent implementation.

### Data

Data is the durable source of truth.

This may eventually include files, Markdown, relational data, object storage, search indexes, or other stores.

### Identity

Identity determines who is requesting an operation.

Future family-agent functionality requires multiple identities and explicit identity boundaries.

### Policy

Policy determines what an identity and agent are allowed to do.

The intended access model is:

```text
Identity
   ->
Policy
   ->
Tool
   ->
Data
```

Agents should not bypass this boundary.

## Public Software / Private Data Boundary

Hiwan AI deliberately separates its public software layer from its private data layer.

```text
                   PUBLIC
GitHub ─────────────────────────────────
  |
  +-- Source Code
  +-- Architecture
  +-- Documentation
  +-- AI Context
  +-- Reviews
  +-- Non-sensitive Learning
                   |
                   | runtime
                   v
               LOCAL HOST
                   |
      +------------+------------+
      |                         |
   PRIVATE                   PRIVATE
Personal Data              Family Data
Memory                     Memory
Documents                  Conversations
Finance                    Sensitive Records
Credentials                Private Media
```

The public repository must never become the storage location for personal or family data.

Private data is accessed through:

```text
Identity -> Policy -> Tool -> Data
```

rather than through direct repository access.

This boundary is a core architectural invariant.

## Local-First Data Tiers

### L0 — Local Only

Highly sensitive information should remain local:

- family data
- private conversations
- credentials
- sensitive personal records
- private documents

### L1 — Local + Encrypted Backup

User-owned durable knowledge may use encrypted backup:

- learning history
- project knowledge
- non-sensitive personal knowledge
- documentation
- structured knowledge

### L2 — Cloud Allowed

Non-sensitive workloads may use cloud services:

- public research
- coding assistance
- public website content
- cloud inference
- public web search

The exact data-classification implementation remains future work.

## Durable Knowledge

Markdown is the current durable knowledge format.

The intended flow is:

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

Knowledge should remain portable across models and frameworks.

## Initial Local AI Runtime

Ollama is the initial local AI runtime.

The first model baseline is currently:

```text
Qwen3.5 27B MLX
```

This is a baseline for experimentation, not a permanent model commitment.

The architecture must remain capable of replacing the model or runtime without redesigning durable knowledge and application-level identity/policy boundaries.

## Current Repository Governance

Architecture changes follow:

```text
IDEA
  |
  v
PROPOSAL
  |
  v
INDEPENDENT REVIEWS
  |
  v
RECONCILIATION
  |
  v
RICHARD DECISION
  |
  v
DECISIONS.md
  |
  v
IMPLEMENTATION
  |
  v
LEARNING / POST-IMPLEMENTATION REVIEW
```

The repository explicitly separates:

```text
Proposal != Review != Decision
```

## Review Dimensions

Meaningful architecture reviews should consider:

- architecture boundaries
- simplicity
- reversibility
- performance
- security
- privacy
- local-first behavior
- OSS/vendor lock-in
- family-agent suitability
- operations
- maintainability
- data portability
- evidence quality

## Current State

Established:

- Apple Silicon development environment
- Homebrew
- Git
- GitHub CLI and SSH authentication
- private GitHub repository
- Python 3.13
- uv
- Node.js/npm
- Docker
- Obsidian
- initial repository governance
- architecture proposal/review process
- Ollama local runtime

Not yet established as permanent architecture:

- agent framework
- PostgreSQL
- vector database
- MCP server architecture
- production API gateway
- production web application
- family identity system
- production memory implementation

## Architectural Principle

The project should grow by adding the smallest boundary necessary to solve a demonstrated problem.

Avoid building infrastructure merely because it may be useful someday.

Prefer:

```text
evidence
  ->
small experiment
  ->
review
  ->
decision
  ->
implementation
```

over premature platform construction.

## Future Direction

The current roadmap is:

```text
Foundation
   ->
Local AI Runtime
   ->
Minimal Agent Loop
   ->
Knowledge Layer
   ->
Memory / Structured Data
   ->
MCP / Tools
   ->
hiwan.ai
   ->
Family Agent
   ->
Continuous Multi-AI Collaboration
```

Each stage should remain independently useful.

## Security Invariant

Private data must not become public merely because the software repository is public.

Public software and private user data are separate architectural layers.

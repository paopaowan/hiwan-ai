# Hiwan AI Consensus Architecture v1.0

**Date:** 2026-10-07  
**Status:** ACCEPTED BY GPT–GEMINI; FINAL AUTHORITY: RICHARD  
**Repository baseline discussed:** `5df0222`  
**Review note:** Gemini's first review was context-based because it could not directly retrieve the repository. Repository/runtime evidence is therefore still required during Phase 1.

## Purpose

This document records the architecture consensus reached after:

1. Gemini independent architecture review.
2. GPT reconciliation.
3. A second GPT–Gemini reconciliation round.
4. Richard's decision to proceed.

The goal is to freeze the minimum executable architecture for Phase 1 and stop expanding theory until implementation evidence requires a change.

## A. Agreed Principles

1. **Local-first and data sovereignty.** Private personal and family data remains local by default.
2. **Public software / private data.** Public source code and architecture do not imply public user data.
3. **Physical separation over repository conventions.** Private runtime data lives outside the Git working tree.
4. **Boundary first, complexity later.** Preserve clean interfaces now; implement the simplest viable behavior behind them.
5. **Execution over specification.** Tracer-bullet evidence takes priority over further architecture speculation.
6. **Resist framework bloat.** Do not introduce large frameworks, protocols, databases, or distributed infrastructure without demonstrated need.
7. **User-owned durable state.** Durable data and memory belong to the user/identity, not to an agent framework.
8. **Human authority.** Richard remains the final architecture decision-maker.

## B. Agreed Current Architecture

```text
                    PUBLIC
                 ~/hiwan-ai
                     |
        +------------+------------+
        |            |            |
      Code      Architecture   Reviews
        |
        v
  Application / Agent
  (transient execution state allowed)
        |
        v
     Identity
  Phase 1: "richard"
        |
        v
      Policy
  Phase 1: minimal allow/deny
        |
        v
       Tool
        |
        +---- Local Python/Node Tool
        +---- HTTP Tool
        +---- MCP Adapter (later)
        |
        v
  Private Data Interface
        |
        v
                  PRIVATE
                  ~/.hiwan
        +----------+-----------+
        |          |           |
      Data       Memory       Logs
        |
        +---- Databases / Indexes later
```

Model path:

```text
Agent
  ->
Thin LLM Client
  ->
Runtime Adapter
  ->
Ollama
  ->
Qwen3.5
```

## C. Architecture Invariants

```text
Public Software != Private Data

Agent != Durable Memory != Durable Data

Agent may hold transient execution state

Identity -> Policy -> Tool -> Data

Tool != MCP

Model != Runtime != Agent

Boundary first, complexity later

Execution evidence > architecture speculation
```

## D. Private Data Boundary

The public repository is:

```text
~/hiwan-ai/
```

Private runtime data is:

```text
~/.hiwan/
```

The Git repository must not be used as the storage location for real personal or family data.

Phase 1 will establish:

```text
~/.hiwan/dev/
~/.hiwan/private/
```

Development defaults to synthetic/test data. Real private data requires an explicit environment choice.

`.gitignore` remains defense-in-depth only. It is not the primary privacy boundary.

Secret scanning should be added now as a low-cost additional safeguard.

## E. Agent / Memory / Data Boundary

### Agent

The Agent may own transient execution state such as:

- current messages
- temporary plans
- tool results
- current execution state
- current working context

The Agent must not own durable user memory or durable user data.

### Data

**Data = durable source-of-truth records.**

Some data may be immutable; other source records may legitimately change over time.

Examples:

- raw conversation transcripts
- documents
- calendar events
- tasks
- account state

### Memory

Memory is durable derived or curated information useful for future reasoning.

Examples:

- learned user preferences
- summaries
- extracted facts
- derived relationships

Both Data and Memory are user-owned durable assets and must remain portable across agent/framework changes.

## F. Identity / Policy Boundary

The architectural access path remains:

```text
Identity -> Policy -> Tool -> Data
```

Phase 1 deliberately implements only the minimum:

```text
context.identity = "richard"
Policy = minimal allow/deny
```

Phase 1 explicitly does **not** implement:

- RBAC
- ABAC
- delegation
- child identity
- family consent engines
- emergency access
- complex approval workflows

The boundary is preserved; the complexity is deferred.

## G. Tool / MCP Boundary

`Tool` is the architectural concept.

MCP is only a protocol/adapter option.

```text
Agent
  ->
Tool Interface
  +-- Local Python Tool
  +-- Local Node Tool
  +-- HTTP Tool
  +-- MCP Adapter (later)
```

Phase 1 does not require a full MCP Server/Client architecture.

## H. Runtime / Model Boundary

Ollama is the initial local runtime, not a permanent platform commitment.

Qwen3.5 is the initial local model baseline.

Phase 1 uses a very thin LLM/runtime boundary:

```text
Agent
  ->
Thin LLM Client
  ->
Ollama Adapter
  ->
Local Model
```

Do not build a generalized multi-provider model platform now.

The abstraction only needs to prevent the Agent from being tightly coupled to Ollama-specific request code.

## I. Persistence Decision for Phase 1

SQLite is the agreed Phase 1 persistence mechanism for the Tracer Bullet.

Rationale:

- single file
- no server dependency
- ACID behavior
- easy inspection/debugging
- portable
- easy to discard or migrate
- substantially lighter than PostgreSQL

PostgreSQL remains deferred until real concurrency, relational complexity, transaction, or multi-user requirements justify it.

Dedicated Vector DB remains deferred until:

1. the knowledge corpus materially outgrows simple context/full-text retrieval, and
2. BM25/full-text retrieval is demonstrated to be insufficient for required semantic matching.

## J. Architecture Decision Threshold

### Normal development

The following do not require a formal multi-AI architecture review:

- bug fixes
- prompt changes
- UI improvements
- adding a small Tool
- refactoring within accepted boundaries
- experiments
- performance tuning

Flow:

```text
IMPLEMENT
  ->
TEST
  ->
LEARNING
```

### High-impact architecture change

Formal review is reserved for changes such as:

- changing local model runtime
- introducing PostgreSQL
- introducing a dedicated Vector DB
- changing memory/data ownership
- changing the Identity/Policy boundary
- changing the Public/Private boundary
- introducing a major agent framework
- introducing cloud storage for private data
- changing the family permission model

Flow:

```text
PROPOSAL
  ->
INDEPENDENT REVIEW
  ->
RICHARD DECISION
  ->
DECISIONS.md
```

## K. What We Build Now

Phase 1 priorities:

1. Physical private data root.
2. Basic secret scanning safeguard.
3. Ollama + Qwen3.5 runtime verification.
4. Minimal LLM Client.
5. Minimal Agent Loop.
6. One Local Tool.
7. Minimal SQLite persistence.
8. End-to-end Tracer Bullet.
9. Measure, learn, and review.

## L. What We Explicitly Defer

Do not build now:

- PostgreSQL
- dedicated Vector DB
- LangChain
- CrewAI
- AutoGen
- full MCP infrastructure
- multi-user authentication system
- RBAC/ABAC
- family consent engine
- child identity system
- delegation workflow
- microservices
- distributed architecture
- cloud private-data synchronization
- heavy observability platform
- production-grade process supervision

## M. Phase 1 Execution Order

```text
Phase 1A
Physical Private Data Root (~/.hiwan/)
    ->
Phase 1B
Verify Ollama + Qwen3.5 Runtime
    ->
Phase 1C
Minimal LLM Client
    ->
Phase 1D
Minimal Agent Loop
    ->
Phase 1E
One Local Tool
    ->
Phase 1F
SQLite Persistence
    ->
Phase 1G
Tracer Bullet End-to-End
    ->
Phase 1H
Measure / Learn / Review
```

## N. Operational Infrastructure Timing

Tracer Bullet phase:

- manual foreground Ollama/runtime processes are acceptable
- console/simple local file logs are acceptable
- production-grade process supervision is deferred
- scheduled backup automation is deferred
- heavy monitoring is deferred

Before the system becomes an always-on personal agent, revisit:

- automatic startup
- process supervision
- scheduled encrypted backup
- structured local logs
- health checks
- recovery procedures

## O. Remaining Disagreements

**GPT–Gemini Architecture Consensus Reached.**

No material architecture disagreement remains for Phase 1.

One terminology refinement is adopted:

> Data is defined as durable source-of-truth records, not necessarily immutable records.

## P. Evidence Still Needed

The earlier Gemini `NEEDS_EVIDENCE` result is interpreted as `NEEDS_REPOSITORY_EVIDENCE`, not architecture rejection.

Phase 1 must produce evidence that:

1. `~/.hiwan/dev/` physically isolates runtime state from the Git repository.
2. the Agent loop functions reliably through Ollama on the target Mac mini.
3. the thin Identity/Policy placeholders do not materially impede the minimal loop.
4. SQLite is sufficient for the initial persistence workload.
5. the Tracer Bullet can run end-to-end without requiring deferred infrastructure.

Architecture should be reopened only when implementation evidence shows that an accepted boundary or decision is inadequate.

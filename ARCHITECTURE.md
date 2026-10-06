# Hiwan AI OS Architecture

## Purpose

This document describes the current architecture of Hiwan AI OS.

It records what the system is today and the stable architectural boundaries we intend to preserve.

Architecture proposals and independent reviews belong under `architecture/`.

## Architectural North Star

```text
hiwan.ai
    ↓
API Gateway
    ↓
Agent Runtime
    ↓
Identity / Policy
    ↓
MCP / Tools
    ↓
Data / Memory
```

Local-first infrastructure is the preferred foundation for private and durable data.

## Core Boundaries

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

The model provides inference.

Models are replaceable and must not own durable user knowledge.

### Runtime

The runtime provides local or remote model execution.

The initial local runtime is Ollama.

### Agent

An agent coordinates reasoning, context, tools, and tasks.

Agent implementations must remain replaceable.

### Tool

Tools provide controlled access to external capabilities and data.

MCP is the preferred interoperability direction for tool integration where appropriate.

### Memory

Memory is a durable knowledge and context layer independent of a specific model or agent.

### Data

Data includes files, documents, structured records, databases, and other user-owned information.

### Identity

Identity determines who is acting.

The eventual family agent must support distinct identities and scopes.

### Policy

Policy determines what an identity is allowed to access or do.

The access model is:

```text
Identity → Policy → Tool → Data
```

High-impact actions should require explicit human approval.

## Local-First Data Tiers

### L0 — Local Only

Examples:

- family-sensitive information
- private conversations
- credentials and secrets
- highly sensitive personal data

### L1 — Local + Encrypted Backup

Examples:

- durable knowledge
- learning history
- project memory
- personal documents

### L2 — Cloud Allowed

Examples:

- non-sensitive inference
- public web research
- coding assistance
- public website functionality

The classification of a specific dataset must be decided before introducing cloud access.

## Current Runtime Direction

The first local AI runtime is Ollama.

The initial baseline model is Qwen3.5 27B MLX on Apple Silicon.

This is an implementation choice for the current experiment, not a permanent model dependency.

## Knowledge and Memory Direction

Durable knowledge should survive model and runtime replacement.

The current human-facing knowledge workflow is:

```text
Obsidian
    ↓
Markdown
    ↓
Git
    ↓
Knowledge Layer
    ↓
Search / Retrieval
    ↓
Agents / hiwan.ai
```

PostgreSQL and vector/search infrastructure will be introduced when concrete requirements justify them.

## Architecture Review

Meaningful architectural changes should follow:

```text
Proposal
    ↓
Independent Reviews
    ↓
Reconciliation
    ↓
Richard Decision
    ↓
DECISIONS.md
    ↓
Implementation
```

See:

- `architecture/README.md`
- `architecture/proposals/README.md`
- `architecture/reviews/PROTOCOL.md`

## Current Status

This document describes the current architectural direction, not every implementation detail.

When a proposal conflicts with this document, the proposal must be treated as a proposal until explicitly accepted and recorded in `DECISIONS.md`.

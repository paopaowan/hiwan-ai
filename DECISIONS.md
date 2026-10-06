# Hiwan AI OS Decisions

This document records accepted architectural and project-level decisions.

A proposal or review does not become a decision until Richard explicitly accepts it.

## Decision Rules

- Decisions are explicit.
- Decisions should be explainable.
- Decisions should identify important trade-offs.
- Reversible decisions should remain easy to change.
- High-impact decisions should be independently reviewed when practical.
- Superseded decisions remain in history rather than being silently deleted.

## Decision 001 — Local-First Architecture

**Date:** 2026-10-06

**Status:** Accepted

Hiwan AI OS will use a local-first architecture.

Private and durable data should remain local whenever practical. Cloud services may be used where the task or data classification permits them.

## Decision 002 — Separate Agent, Model, Memory, and Data

**Date:** 2026-10-06

**Status:** Accepted

Agents, models, runtimes, memory, and durable data are separate architectural concerns.

No single model or agent framework should become the owner of long-lived user knowledge.

## Decision 003 — Identity → Policy → Tool → Data

**Date:** 2026-10-06

**Status:** Accepted

Access to data and capabilities should follow:

```text
Identity → Policy → Tool → Data
```

This is a foundational requirement for the eventual family-agent architecture.

## Decision 004 — Markdown as a Durable Knowledge Format

**Date:** 2026-10-06

**Status:** Accepted

Markdown is the initial durable human-readable knowledge format.

Git is used for version history.

Obsidian is the initial human-facing Markdown tool.

## Decision 005 — Python 3.13 and uv

**Date:** 2026-10-06

**Status:** Accepted

Python 3.13 is the initial Python version.

uv is the preferred Python environment and dependency management tool.

## Decision 006 — Ollama as Initial Local AI Runtime

**Date:** 2026-10-06

**Status:** Accepted

Ollama is the first local AI runtime used for experimentation and development.

This decision does not prevent replacing Ollama later.

The runtime must remain behind a replaceable interface so that agents do not depend directly on Ollama-specific behavior where avoidable.

## Decision 007 — Avoid Premature Agent Framework Lock-In

**Date:** 2026-10-06

**Status:** Accepted

Hiwan AI OS will not adopt a large agent framework merely because it is popular.

A framework should be introduced only when a concrete requirement demonstrates that its capabilities justify the additional abstraction and dependency surface.

## Decision 008 — Multi-AI Independent Architecture Review

**Date:** 2026-10-06

**Status:** Accepted

Meaningful architecture proposals may be reviewed independently by multiple AI systems.

The purpose is to expose blind spots and alternatives, not to create automatic consensus.

Richard remains the final decision-maker.

The review process is defined in:

`architecture/reviews/PROTOCOL.md`

## Decision 009 — Learning Includes Failures and Gotchas

**Date:** 2026-10-06

**Status:** Accepted

Learning records should preserve not only successful implementation steps, but also failures, gotchas, decisions, assumptions, and questions.

This creates durable engineering knowledge for future work and future AI collaborators.

## Decision Lifecycle

```text
Proposal
    ↓
Review
    ↓
Richard Decision
    ↓
This file
    ↓
Implementation
    ↓
Learning / Post-Implementation Review
```

## Future Decisions

New accepted decisions should be added with:

- decision number
- date
- status
- context
- decision
- important trade-offs
- consequences
- supersession information when applicable

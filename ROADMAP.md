# Hiwan AI OS Roadmap

## Purpose

This roadmap describes the intended evolution of Hiwan AI OS.

It is directional rather than a promise of exact dates.

Architecture proposals and reviews may change the roadmap before implementation.

## Phase 0 — Foundation

**Status:** Completed

- Apple Silicon development environment
- Homebrew
- Git and GitHub CLI
- Private GitHub repository
- Python 3.13
- uv
- Node.js / npm
- Docker
- Obsidian
- Learning journal
- AI project context
- Architecture review protocol

## Phase 1 — Local AI Runtime

**Status:** In Progress

Goals:

- install and validate Ollama
- install and benchmark an initial local model
- understand local model API behavior
- verify inference performance on Apple Silicon
- create a minimal Python client
- keep the model/runtime boundary replaceable

Initial experiment:

- Ollama
- Qwen3.5 27B MLX

## Phase 2 — Minimal Agent Loop

**Status:** Planned

Goals:

- define the smallest useful agent loop
- model request/response abstraction
- tool invocation boundary
- structured context
- basic logging
- failure handling
- human approval boundary

Do not introduce a large agent framework unless Phase 2 requirements justify it.

## Phase 3 — Knowledge Layer

**Status:** Planned

Goals:

- connect Markdown knowledge
- define knowledge metadata
- searchable local knowledge
- retrieval experiments
- source attribution
- distinguish knowledge from conversational memory

## Phase 4 — Memory and Structured Data

**Status:** Planned

Goals:

- define memory schemas
- evaluate PostgreSQL
- evaluate search/vector requirements
- define retention and deletion rules
- preserve data portability

## Phase 5 — MCP and Tool Layer

**Status:** Planned

Goals:

- local MCP/tool experiments
- explicit tool permissions
- tool audit trail
- identity-aware access
- safe external actions

## Phase 6 — hiwan.ai

**Status:** Planned

Goals:

- user-facing web application
- authentication
- conversation interface
- learning view
- knowledge view
- agent/task visibility
- approval workflows

## Phase 7 — Family Agent

**Status:** Future

Goals:

- multiple identities
- family-specific policies
- scoped memory
- shared vs private knowledge
- human approval for high-impact actions
- family-safe tool access

## Phase 8 — Continuous AI Collaboration

**Status:** Future

Goals:

- GPT / Gemini / Claude independent reviews
- proposal/review/decision workflow
- automated repository context
- architecture regression checks
- knowledge synchronization

## Current Priority

The immediate priority is:

```text
Local AI Runtime
    ↓
Minimal Agent Loop
    ↓
Knowledge Layer
    ↓
Memory / Data
    ↓
Tools / MCP
    ↓
hiwan.ai
    ↓
Family Agent
```

Infrastructure should be introduced only when justified by the next concrete requirement.

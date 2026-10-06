# AI_CONTEXT.md

> Hiwan AI OS — shared context for AI assistants
>
> Version: 1.0
> Status: Active
> Last reviewed: 2026-10-06
> Source of truth: repository files + Git history; this file is a concise synthesis.

## 1. What this project is

Hiwan AI OS is Richard's long-term local-first AI ecosystem.

The immediate project is not to build a single chatbot. The intended destination is a modular personal/family AI system in which models, agents, tools, memory, identity, permissions, and durable knowledge can evolve independently.

## 2. Why it exists

The project started from the desire to have a capable personal AI assistant and is deliberately evolving toward a family agent.

The important architectural insight is that an agent should not own the user's long-lived knowledge or identity. Models and runtimes will change; durable knowledge and permissions must survive those changes.

## 3. Architectural north star

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
             ┌─────────┼─────────┐
             ↓         ↓         ↓
        PostgreSQL   Files    Markdown
             ↓
       Search / RAG later
```

Possible specialized agents:

- Personal
- Family
- Language
- Education
- Finance
- Research
- Coding

These are planned boundaries, not necessarily separate deployed services.

## 4. Core separation

The project explicitly separates:

```text
Model      = reasoning / generation capability
Runtime    = model serving infrastructure
Agent      = task-oriented behavior and orchestration
Tool       = controlled external capability
Memory     = durable contextual information
Data       = source-of-truth records/files
Identity   = who is acting
Policy     = what that identity is allowed to do
```

A key invariant is:

```text
Identity → Policy → Tool → Data
```

An AI should not jump directly from natural language to sensitive data or high-impact external actions.

## 5. Local-first data model

The current conceptual tiers are:

### L0 — local only

Highly private material such as family-sensitive information, secrets, private conversations, credentials, and other data that should not leave the trusted local environment.

### L1 — local + encrypted backup

Durable knowledge, learning notes, project memory, documents, and other valuable data that benefits from backup but should remain under user control.

### L2 — cloud-permitted

Tasks such as public web research, non-sensitive inference, coding assistance, and other workloads where cloud services provide clear value and the data is appropriate to send.

These are policy concepts, not yet an implemented policy engine.

## 6. Knowledge and learning strategy

Human-facing knowledge is intended to remain Markdown-first and Git-friendly.

Current direction:

```text
Obsidian
   ↓
Markdown
   ↓
Git
   ↓
Knowledge Layer
   ↓
Search / RAG when justified
   ↓
hiwan.ai /learning and agent context
```

Learning notes deliberately record:

- Learned
- Built
- Understood
- Failed
- Gotchas
- Decisions
- Questions
- Next
- Commands

Failures and gotchas are treated as valuable engineering knowledge rather than noise.

## 7. Environment established

The development environment has been intentionally kept simple:

- Apple Silicon Mac mini, M5 Pro, 64 GB unified memory
- Homebrew
- Git + GitHub CLI
- Private GitHub repository
- Python 3.13
- uv
- project `.venv`
- Node.js/npm
- Docker/Compose
- Obsidian
- Ollama

Exact installed versions should be verified from the machine when they matter; do not treat historical version numbers in this file as authoritative.

## 8. Local AI runtime stage

Ollama is the first local model runtime.

Reasoning:

- simple installation
- local HTTP API
- easy model replacement
- useful for early experiments
- keeps the agent architecture independent of the runtime
- avoids committing to a large orchestration framework too early

The first model under evaluation is Qwen3.5 27B MLX for Apple Silicon.

The runtime/model choice is an experiment and benchmark baseline, not a permanent architectural commitment.

## 9. What has deliberately NOT been chosen

At this stage, do not assume that the project requires:

- LangChain
- CrewAI
- Open WebUI
- a vector database
- PostgreSQL immediately
- a particular MCP server framework
- a particular agent runtime/framework
- a particular cloud model provider

The test is always:

> What concrete requirement does this component solve, and can we keep the boundary replaceable?

## 10. Current open questions

1. What is the smallest useful local agent loop?
2. Which local model/runtime combination gives the best quality, latency, and memory trade-off on this hardware?
3. When should PostgreSQL be introduced?
4. What is the minimum useful memory/search layer before adding vector infrastructure?
5. How should Markdown knowledge become searchable agent context?
6. How should MCP tools express identity and permissions?
7. What family-agent actions require explicit human approval?
8. How should knowledge extraction from conversations be made reliable and auditable?
9. What should remain local versus cloud-permitted?

## 11. Important historical lessons

The setup phase exposed several durable engineering lessons:

- Terminal heredocs are fragile when exact delimiters are mishandled.
- A successful shell command does not prove the intended file was changed.
- Always verify with `git status`, file inspection, and where useful local/remote commit SHA.
- `uv` is the preferred Python environment/dependency workflow.
- A newly created Python venv may not contain `pip`; install it explicitly only when needed.
- Docker installation is not enough; `docker info` verifies the engine is actually running.
- GitHub authentication can succeed through browser/device flow even when an initial identity assumption fails.
- Keep copy/paste workflows compact and verify results immediately.
- Do not treat an AI-generated command/output as correct merely because it looks plausible.

## 12. How to challenge this context

An AI should actively challenge this project when it detects:

- unnecessary complexity
- contradictory architectural boundaries
- unjustified framework adoption
- privacy/security weaknesses
- vendor lock-in
- an abstraction that is too early
- a decision that conflicts with the actual implementation
- a requirement that is being solved before it is understood

A disagreement is useful if it is explicit and evidence-based.

## 13. Maintenance rules

This document is a synthesis, not a diary.

Update it when:

- the north-star architecture materially changes
- a major technology is adopted or removed
- a major invariant changes
- the current stage changes
- an important open question is resolved

Do not append every daily command here. Put daily detail in `learning/YYYY-MM-DD.md`.

## 14. Confidence labels

When adding important information, use one of:

- **FACT** — directly verified in repository, machine, documentation, or explicit decision.
- **DECISION** — deliberately chosen by Richard.
- **PROPOSAL** — suggested but not accepted.
- **ASSUMPTION** — currently believed but not verified.
- **OPEN** — unresolved question.

This prevents AI assistants from converting guesses into project history.

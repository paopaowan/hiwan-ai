# Architecture Proposals & Reviews

This directory is the evidence trail for meaningful Hiwan AI OS architecture changes.

## Core rule

```text
Proposal != Review != Decision
```

A proposal describes a possible change.
A review independently evaluates it.
The final decision is made by Richard and recorded in `DECISIONS.md`.

## Directory structure

```text
architecture/
├── proposals/
│   ├── README.md
│   ├── TEMPLATE.md
│   └── YYYY-MM-DD-<slug>.md
│
└── reviews/
    ├── README.md
    ├── PROTOCOL.md
    ├── gpt/
    ├── gemini/
    ├── claude/
    └── other/
```

## Naming

Proposal:

`YYYY-MM-DD-<short-slug>.md`

Review:

`YYYY-MM-DD-<proposal-slug>--<reviewer>.md`

Examples:

```text
proposals/2026-10-07-local-agent-runtime.md

reviews/gpt/2026-10-07-local-agent-runtime--gpt.md
reviews/gemini/2026-10-07-local-agent-runtime--gemini.md
reviews/claude/2026-10-07-local-agent-runtime--claude.md
```

## Lifecycle

```text
IDEA
  ↓
PROPOSAL
  ↓
INDEPENDENT REVIEWS
  ├── GPT
  ├── Gemini
  ├── Claude
  └── Other
  ↓
RECONCILIATION
  ↓
RICHARD DECISION
  ↓
DECISIONS.md
  ↓
IMPLEMENTATION
  ↓
LEARNING / POST-IMPLEMENTATION REVIEW
```

A proposal may be rejected or deferred. It does not have to become an implementation.

## Status vocabulary

Use exactly one proposal status:

- `DRAFT`
- `IN_REVIEW`
- `REVISED`
- `DECIDED`
- `IMPLEMENTED`
- `DEFERRED`
- `REJECTED`
- `SUPERSEDED`

Use exactly one review verdict:

- `APPROVE`
- `APPROVE_WITH_CONDITIONS`
- `DEFER`
- `REJECT`
- `NEEDS_EVIDENCE`

Use `DECISIONS.md` as the authoritative record of accepted project decisions.

## Evidence levels

Reviewers should distinguish:

- `FACT` — verified from source/repository/current documentation.
- `DECISION` — explicitly accepted by Richard.
- `PROPOSAL` — suggested but not accepted.
- `ASSUMPTION` — plausible but unverified.
- `OPEN` — unresolved.

Never convert a proposal or assumption into a fact.

## Independence rule

Each reviewer should first inspect the proposal and project context independently.

Do not copy another review before forming an initial position.

If reviews disagree, preserve the disagreement. Do not erase it by averaging opinions.

## What belongs here

Good candidates:

- agent runtime
- model/runtime strategy
- memory architecture
- data architecture
- MCP/tool architecture
- identity/permission model
- family-agent boundaries
- cloud/local data movement
- major infrastructure choices
- new frameworks with architectural consequences
- security/privacy architecture

Do not create proposals for:

- trivial bug fixes
- formatting
- routine dependency updates
- ordinary documentation edits
- one-line implementation details

## Final principle

The purpose of this directory is not bureaucracy.

Its purpose is to make architectural reasoning:

- inspectable
- reversible
- evidence-based
- multi-model reviewed
- historically traceable

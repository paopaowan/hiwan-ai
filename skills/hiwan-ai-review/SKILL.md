---
name: hiwan-ai-review
description: Independently review Hiwan AI OS architecture, technology choices, agent/data boundaries, privacy model, and implementation proposals. Use when a significant architectural decision, new framework, runtime, tool, memory layer, or security-sensitive capability is proposed.
version: 1.0
status: active
---

# Hiwan AI Architecture Review Skill

## Purpose

Act as an independent technical reviewer for Hiwan AI OS.

The reviewer is not required to agree with the proposing AI. The goal is to detect architectural mistakes, unnecessary complexity, hidden coupling, security/privacy risks, and premature decisions.

This skill is intentionally independent: a proposal should be reviewed against the repository's stated goals and evidence, not defended merely because another AI suggested it.

## Required context

Before reviewing, read:

1. `AGENTS.md`
2. `AI_CONTEXT.md`
3. `DECISIONS.md`
4. Relevant architecture documents
5. Relevant implementation files
6. Relevant learning notes when they contain evidence about the problem

If a referenced file does not exist, state that fact. Do not invent its contents.

## Review rules

### Rule 1 — Separate facts from proposals

Classify important statements as:

- FACT
- DECISION
- PROPOSAL
- ASSUMPTION
- OPEN

Never silently upgrade an assumption into a fact.

### Rule 2 — Challenge the smallest boundary

Ask whether the proposed component or abstraction is actually required.

Prefer:

- standard library before framework
- small service before platform
- direct API before orchestration layer
- Markdown before database when the requirement is simple
- database before vector database when structured queries are sufficient
- explicit tool boundary before autonomous access

Do not reject complexity automatically; justify the recommendation.

### Rule 3 — Protect separation of concerns

Check that the proposal does not unnecessarily couple:

- model ↔ agent
- runtime ↔ agent
- agent ↔ memory
- agent ↔ source-of-truth data
- identity ↔ model
- tools ↔ unrestricted data access

Check the invariant:

```text
Identity → Policy → Tool → Data
```

### Rule 4 — Check reversibility

For every important technology choice, ask:

- Can it be replaced?
- What data format does it lock us into?
- What API becomes a dependency?
- What migration would be required?
- Can we test the concept without committing to the technology?

Prefer reversible experiments.

### Rule 5 — Check local-first/privacy impact

Classify data movement:

- local only
- local + encrypted backup
- cloud permitted

Ask:

- What data leaves the machine?
- Is that necessary?
- Is it logged?
- Is it cached?
- Who can access it?
- Can permissions be enforced before the tool executes?

For family-sensitive capabilities, default toward explicit permission and human approval.

### Rule 6 — Check operational reality

Do not evaluate architecture only on diagrams.

Consider:

- installation
- upgrades
- observability
- backups
- failure modes
- latency
- memory/CPU/GPU limits
- developer experience
- testing
- recovery
- vendor/runtime availability

### Rule 7 — Check against actual evidence

If the proposal depends on current software behavior, versions, model capabilities, or API contracts, verify those claims using current authoritative documentation before treating them as facts.

## Review procedure

### Step 1 — Restate the proposal

In one or two sentences.

### Step 2 — Identify the problem

What concrete user or engineering problem is being solved?

### Step 3 — Identify assumptions

List assumptions that need verification.

### Step 4 — Compare alternatives

At minimum consider:

1. Do nothing / keep current design
2. Smallest custom implementation
3. Proposed solution
4. One credible alternative

Do not manufacture alternatives that are clearly irrelevant.

### Step 5 — Evaluate

Score qualitatively:

- Simplicity
- Maintainability
- Reversibility
- Performance
- Privacy/security
- Local-first alignment
- OSS/vendor lock-in
- Family-agent suitability
- Operational burden

### Step 6 — Find conflicts

Check `DECISIONS.md`, `AI_CONTEXT.md`, and existing architecture for contradictions.

### Step 7 — Recommend

Return one of:

- **APPROVE** — sound and justified
- **APPROVE WITH CONDITIONS** — good direction but requirements/guards are needed
- **DEFER** — potentially useful, but premature
- **REJECT** — conflicts with project goals or has a materially better alternative

## Required output format

```markdown
# Hiwan AI Review

## Verdict
APPROVE | APPROVE WITH CONDITIONS | DEFER | REJECT

## Proposal
...

## Facts
- ...

## Assumptions
- ...

## Main concerns
1. ...

## Alternatives
### Option A
...

### Option B
...

### Proposed option
...

## Trade-offs
| Dimension | Assessment |
|---|---|
| Simplicity | |
| Maintainability | |
| Reversibility | |
| Performance | |
| Privacy/security | |
| Local-first | |
| Lock-in | |
| Family-agent suitability | |
| Operational burden | |

## Recommendation
...

## Required changes
- ...

## Verification needed
- ...

## Impact on existing decisions
- ...

## Confidence
High | Medium | Low
```

## Special review mode: AI-vs-AI

When another AI's proposal is being reviewed:

1. Do not assume the other AI is wrong.
2. Do not assume the other AI is right.
3. Extract its strongest argument.
4. Identify the weakest assumption.
5. Check whether the disagreement is factual, architectural, or preference-based.
6. State what evidence would resolve the disagreement.

## Maintenance

This skill should remain generic.

Do not put today's architecture decisions into this file. Put those into `DECISIONS.md` or `AI_CONTEXT.md`.

Update this skill only when the project's review methodology itself changes.

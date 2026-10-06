# Review Protocol v1.0

> Hiwan AI OS — Multi-model Architecture Review Protocol
>
> Version: 1.0
> Status: Active
> Owner: Richard
> Last reviewed: 2026-10-06

## 1. Purpose

This protocol provides a repeatable process for evaluating meaningful architecture proposals using multiple independent AI reviewers.

The objective is not consensus for its own sake.

The objective is to expose:

- incorrect assumptions
- unnecessary complexity
- hidden coupling
- security/privacy risks
- operational costs
- vendor lock-in
- premature abstractions
- conflicts with existing decisions
- better alternatives

## 2. Authority model

```text
AI proposes
   ↓
AI reviews
   ↓
AI reviews disagree where appropriate
   ↓
Evidence is reconciled
   ↓
Richard decides
   ↓
DECISIONS.md becomes authoritative
```

AI reviewers have no authority to silently change architecture.

## 3. When a review is required

Use this protocol when a proposal materially affects:

- system architecture
- model/runtime selection
- agent orchestration
- memory
- durable data
- MCP/tools
- identity
- permissions
- family-agent behavior
- cloud/local boundaries
- security/privacy
- major dependencies/frameworks
- infrastructure
- irreversible or expensive migrations

A review is optional for routine implementation work.

## 4. Required context

Before reviewing, read:

1. `AGENTS.md`
2. `AI_CONTEXT.md`
3. `DECISIONS.md`
4. The target proposal
5. Relevant architecture documents
6. Relevant implementation files
7. Relevant learning notes

If current external software behavior matters, verify against current authoritative documentation.

## 5. Review phases

### Phase 0 — Prepare

Confirm:

- proposal exists
- proposal status is `IN_REVIEW`
- proposal has a clear problem
- alternatives are documented
- affected boundaries are identified

### Phase 1 — Independent review

Each reviewer produces its own review without relying on another reviewer's conclusion.

Minimum reviewers for high-impact decisions:

- GPT
- Gemini
- Claude

For smaller decisions, one independent reviewer may be sufficient.

### Phase 2 — Compare

After independent reviews are complete, identify:

- agreement
- disagreement
- unique concerns
- evidence gaps
- factual conflicts
- preference-based differences

### Phase 3 — Reconcile

Do not force a false consensus.

Classify each disagreement:

- `FACTUAL` — can be resolved by evidence.
- `ARCHITECTURAL` — depends on system trade-offs.
- `PREFERENCE` — multiple valid choices exist.
- `UNKNOWN` — insufficient evidence.

### Phase 4 — Decision

Richard decides.

Possible decisions:

- `APPROVED`
- `APPROVED WITH CONDITIONS`
- `DEFERRED`
- `REJECTED`

The decision must be recorded in `DECISIONS.md`.

### Phase 5 — Implementation

Only after the decision should implementation become the normal next step.

The proposal status becomes `DECIDED`, then `IMPLEMENTED` when the implementation is actually complete.

### Phase 6 — Post-implementation

For high-impact decisions, record:

- what happened
- whether assumptions were correct
- unexpected problems
- performance/operational results
- whether the decision should remain

Use `learning/` for detailed lessons and update `DECISIONS.md` if the decision changes.

## 6. Review dimensions

Every reviewer should consider:

### Architecture

- Does the proposal preserve separation of concerns?
- Does it create hidden coupling?
- Does it introduce an abstraction too early?

### Simplicity

- Is there a simpler solution?
- Is complexity proportional to the problem?

### Reversibility

- Can it be removed?
- Is data portable?
- Is migration practical?

### Performance

- Latency
- throughput
- memory
- CPU/GPU requirements
- local hardware constraints

### Security

- identity
- authorization
- secrets
- tool permissions
- destructive actions
- auditability

### Privacy

- what data leaves local infrastructure?
- is cloud processing necessary?
- is sensitive/family data exposed?

### Local-first alignment

- Can the capability work locally?
- If cloud is used, is the boundary explicit?

### OSS / vendor lock-in

- Is the dependency replaceable?
- Does it impose proprietary formats/APIs?
- Is the project becoming dependent on one provider?

### Family-agent suitability

- Can identities be separated?
- Can permissions differ by person?
- Can high-impact actions require approval?
- Can private family data remain isolated?

### Operations

- installation
- upgrades
- backups
- observability
- testing
- failure recovery

## 7. Reviewer output

Every review must use this structure:

```markdown
# Architecture Review

> Proposal: <proposal id>
> Reviewer: <GPT | Gemini | Claude | Other>
> Date: YYYY-MM-DD
> Protocol: v1.0

## Verdict

APPROVE | APPROVE_WITH_CONDITIONS | DEFER | REJECT | NEEDS_EVIDENCE

## 1. Proposal understood

...

## 2. Facts

- ...

## 3. Assumptions

- ...

## 4. Strongest argument for the proposal

...

## 5. Main concerns

1. ...

## 6. Alternatives

### Keep current design

...

### Proposed design

...

### Alternative

...

## 7. Trade-offs

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
| Operations | |

## 8. Evidence needed

- ...

## 9. Recommendation

...

## 10. Impact on existing decisions

...

## 11. Confidence

High | Medium | Low
```

## 8. Anti-bias requirements

Reviewers must explicitly answer:

1. What could the proposing AI be wrong about?
2. What could the reviewer itself be wrong about?
3. Which claim most needs external verification?
4. What is the simplest credible alternative?
5. What evidence would change the verdict?

This prevents the review process from becoming AI-to-AI confirmation.

## 9. Evidence rules

When current technical behavior matters:

- prefer official documentation
- prefer primary sources
- record the relevant version
- distinguish documentation claims from observed behavior
- do not cite an old benchmark as current fact without qualification

If a claim cannot be verified, mark it `ASSUMPTION` or `NEEDS_EVIDENCE`.

## 10. Conflict handling

If GPT says APPROVE and Gemini says REJECT:

Do not average them to "mostly approve."

Instead:

```text
Conflict
  ↓
Identify exact disagreement
  ↓
Classify: FACTUAL / ARCHITECTURAL / PREFERENCE / UNKNOWN
  ↓
Collect evidence
  ↓
Richard decides
```

## 11. Decision recording

After Richard decides, update `DECISIONS.md` with:

- date
- decision
- context
- alternatives
- rationale
- reviewers
- conditions
- consequences

The proposal remains the detailed historical record.

## 12. Review quality bar

A high-quality review should make the proposal better even when the verdict is APPROVE.

A review that only says:

> "Looks good."

is not considered sufficient for a high-impact decision.

## 13. Versioning

Protocol changes are versioned:

- `1.x` — compatible process improvements
- `2.0` — materially different review authority, lifecycle, or output contract

Review documents record the protocol version used.

## 14. Long-term principle

The review system exists to preserve human agency and architectural quality.

It must never become a mechanism for outsourcing final technical judgment to whichever AI sounds most confident.

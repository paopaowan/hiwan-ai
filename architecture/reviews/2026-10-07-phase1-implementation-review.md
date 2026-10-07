# Hiwan AI Phase 1 Implementation Review

**Date:** 2026-10-07
**Status:** PHASE 1G PASSED / PHASE 1H REVIEW
**Implementation baseline:** `d9b60a1`
**Review scope:** Phase 1A through Phase 1G

## Executive Summary

Hiwan AI has completed its first end-to-end local-first Agent tracer bullet.

The implementation now proves that the following components can operate together on the target Mac mini:

```text
User Prompt
  ->
Agent
  ->
Identity
  ->
Minimal Policy
  ->
LLM Tool Router
  ->
Local Tool
  ->
Tool Result
  ->
Qwen3.5 Final Answer
  ->
SQLite Persistence
```

Private runtime data is physically stored outside the public Git repository.

The implementation supports the core GPT–Gemini Consensus Architecture v1.0 sufficiently to proceed beyond pure architecture design.

However, the result is still a Phase 1 tracer bullet rather than a production-ready personal Agent.

The most important remaining work is reliability, failure handling, auditability, and knowledge retrieval—not additional architectural layers.

## 1. Verified Implementation Evidence

### Repository / Private Data Boundary

Verified:

```text
Public repository:
/Users/richard/hiwan-ai

Private runtime root:
/Users/richard/.hiwan
```

Result:

```text
PASS: private data is physically outside Git repository
```

Private root permissions:

```text
drwx------
```

SQLite database permissions:

```text
-rw-------
```

### Secret Scanning

Homebrew Gitleaks `8.30.1` failed a positive-control synthetic GitHub PAT test.

A pinned Gitleaks `8.18.4` was installed separately and passed the same positive-control test.

Trusted scanner:

```text
~/.local/bin/gitleaks-hiwan
```

Repository scan:

```text
8 commits scanned
no leaks found
```

Working tree scan:

```text
no leaks found
```

Pre-commit positive-control:

```text
PASS: pre-commit blocked the synthetic secret
```

Clean staged-state:

```text
PASS: clean staged state is allowed
```

### Local Model Runtime

Verified baseline:

```text
Runtime: Ollama 0.40.0
Model: qwen3.5:27b-mlx
Runner: MLX
Processor: 100% GPU
Context baseline: 8192
Runtime resident size: ~20 GB
```

Cold run:

```text
Total: 6.614 s
Load: 2.336 s
Generation: 15.72 tok/s
```

Warm run:

```text
Total: 2.190 s
Load: 0.028 s
Generation: 16.03 tok/s
```

Deterministic no-thinking functional test:

```text
Response: HIWAN_LOCAL_AI_OK
Thinking chars: 0
Done reason: stop
PASS
```

### Minimal LLM Client

Verified:

```text
1 unit test passed
live Ollama smoke test passed
```

No external Python LLM framework was required.

### Minimal Agent Loop

Verified:

```text
4 unit tests passed
Identity: richard
Response: HIWAN_AGENT_OK
PASS
```

### First Local Tool

Tool:

```text
local_system_info
```

Verified:

```text
7 unit tests passed
Tool used: local_system_info
Tool result: os=Darwin release=27.0.0 architecture=arm64
PASS
```

### SQLite Persistence

Database:

```text
~/.hiwan/dev/databases/hiwan.db
```

Verified:

```text
9 unit tests passed
write succeeded
read-back succeeded
Inside Git repo: False
PASS
```

### End-to-End Tracer Bullet

Verified:

```text
10 unit tests passed
Run count before: 1
Run count after: 2
Identity: richard
Tool used: local_system_info
Tool result: architecture=arm64
Persisted identity: richard
Persisted tool: local_system_info
Persisted status: ok
Database inside Git repo: False
PASS
```

Commit:

```text
d9b60a1 feat: complete first end-to-end agent tracer bullet
```

Local and remote SHA matched:

```text
d9b60a12b0d59b2012031f239b151e331005a695
```

## 2. Consensus Assumptions Now Supported by Evidence

### Public Software != Private Data

**Status:** SUPPORTED

Private runtime data is physically outside the Git working tree.

### Agent != Durable Memory != Durable Data

**Status:** PARTIALLY SUPPORTED

The current Agent holds transient execution state while SQLite persistence is managed by a separate storage component.

Durable Memory itself has not yet been implemented, so the complete Memory/Data distinction still requires future evidence.

### Identity -> Policy -> Tool -> Data

**Status:** PARTIALLY SUPPORTED

The implementation preserves:

```text
Identity = richard
Policy = minimal allow/deny
Tool = local_system_info
```

The current Policy is intentionally simple.

Family/multi-user authorization is not implemented and is correctly deferred.

### Tool != MCP

**Status:** SUPPORTED

The first real Tool operates successfully without MCP.

MCP remains a future adapter option.

### Model != Runtime != Agent

**Status:** SUPPORTED

The current implementation separates:

```text
Agent
  ->
OllamaClient
  ->
Ollama
  ->
Qwen3.5
```

### Thin Runtime Abstraction

**Status:** SUPPORTED

The standard-library Ollama client was sufficient for Phase 1.

There is no evidence requiring a generalized multi-provider model framework.

### SQLite Before PostgreSQL

**Status:** SUPPORTED FOR CURRENT WORKLOAD

SQLite successfully persists current single-user Agent runs.

There is no current evidence requiring PostgreSQL.

### No Dedicated Vector DB Yet

**Status:** SUPPORTED

No current Phase 1 requirement depended on vector search.

## 3. Important Evidence Against Blind Assumptions

### Security Scanner Regression

Gitleaks `8.30.1` failed a synthetic-secret positive control.

Lesson:

```text
Security tool output is not evidence
until the security tool itself passes a positive-control test.
```

This supports an evidence-first engineering culture.

### Thinking Token Budget

The initial Qwen test produced no final content because thinking consumed the short generation budget.

This shows model behavior must be measured rather than assumed.

### Tool Routing Is Still Fragile

The current Tool Router depends on model-generated JSON parsed with:

```text
json.loads(...)
```

This works for the tracer bullet but is not yet robust production behavior.

## 4. Current Strengths

1. The public/private data boundary is physically enforced.
2. The repository has a validated secret-scanning gate.
3. The local model runtime is proven on target hardware.
4. The Agent remains small and inspectable.
5. Identity/Policy boundaries exist without premature authorization complexity.
6. The Tool abstraction is proven independently of MCP.
7. Persistence is outside Git and user-owned.
8. The implementation avoids framework lock-in.
9. Unit tests grew with each implementation stage.
10. The complete tracer bullet is now operational.

## 5. Current Reliability Gaps

### Tool Router Invalid JSON

Current behavior:

```text
invalid JSON -> RuntimeError
```

Needed later:

- bounded retry or correction strategy
- structured-output evaluation
- clear failure record

### Unknown Tool

Current behavior rejects unknown Tool names.

Needed later:

- explicit typed failure
- persisted failure status
- possibly a safe fallback response

### Ollama Unavailable

The LLM client surfaces runtime errors.

Still needed:

- end-to-end failure test
- clear user-facing failure behavior
- persistence of failed runs

### Model Timeout / Long Generation

Timeout configuration exists in the client.

Still needed:

- timeout test
- runtime-level error status
- retry policy decision

### Persistence Failure

Current happy path assumes SQLite write succeeds.

Still needed:

- disk/database failure behavior
- transaction/error tests
- decision on response delivery if persistence fails

## 6. Current Security / Privacy Gaps

### Local Git Hook Is Machine-Local

The current pre-commit hook is effective on Richard's Mac mini but is not automatically installed for another contributor or machine.

This is acceptable for the current single-owner Phase 1.

Revisit before multi-developer collaboration.

### Secret Scanner Version Pin

The trusted scanner is pinned outside Homebrew:

```text
~/.local/bin/gitleaks-hiwan
```

A future setup/bootstrap mechanism should reproduce this validation.

### Private Environment Not Used Yet

Phase 1 tests operate in:

```text
~/.hiwan/dev/
```

This is desirable.

Real private data should remain unused until failure handling and environment selection are stronger.

### Audit Log

Current SQLite records are normal mutable database rows.

Family-agent auditability may eventually require append-only or tamper-evident records.

Not required now.

## 7. Performance Evidence

Current known Qwen3.5 27B MLX baseline:

```text
Cold total: 6.614 s
Cold load: 2.336 s
Warm total: 2.190 s
Warm load: 0.028 s
Generation: ~16 tok/s
Context baseline: 8192
GPU: 100%
```

Interpretation:

- warm local interaction is practical for Phase 1
- cold load cost is acceptable for development
- this is not yet a long-duration stability benchmark
- this does not prove performance at very large context sizes
- this does not prove multi-agent concurrency

## 8. Architecture Changes Required?

**Verdict:** NO MAJOR ARCHITECTURE CHANGE REQUIRED

The Phase 1 evidence supports the current Consensus Architecture.

No evidence currently justifies:

- PostgreSQL
- Vector DB
- LangChain
- CrewAI
- AutoGen
- full MCP infrastructure
- microservices
- distributed runtime
- full RBAC/ABAC
- Family identity implementation
- heavy observability platform

## 9. What Should Be Improved Before Real Private Data

The following should be addressed before moving meaningful real personal/family data into the system:

1. failed Agent-run persistence
2. Tool Router malformed-output handling
3. Ollama unavailable/timeout path
4. explicit dev/private environment selection
5. backup/recovery plan for private data
6. minimal audit/event logging policy
7. secret-scanner bootstrap/reproducibility

These improvements do not require reopening the overall architecture.

## 10. Recommended Next Direction

Do not add another infrastructure layer immediately.

The next major product capability should be the **Knowledge Layer**, starting from existing Markdown.

Recommended sequence:

```text
Markdown files
  ->
simple discovery
  ->
simple full-text retrieval
  ->
Agent context injection
  ->
measure usefulness
```

Do not start with embeddings or a dedicated Vector DB.

The Knowledge Layer should first prove that:

1. the Agent can discover user-owned Markdown,
2. retrieve relevant text,
3. cite/identify its source,
4. use it in an answer,
5. keep durable knowledge independent from the Agent framework.

## 11. Phase 1H Verdict

```text
PHASE 1 TRACER BULLET: PASS
CONSENSUS ARCHITECTURE: SUPPORTED BY IMPLEMENTATION EVIDENCE
MAJOR REDESIGN REQUIRED: NO
READY FOR KNOWLEDGE-LAYER PLANNING: YES
READY FOR REAL PRIVATE/FAMILY DATA: NOT YET
```

## 12. Evidence Still Needed

Future evidence should test:

- repeated Tool Router reliability
- malformed LLM structured output
- unknown Tool behavior
- Ollama unavailable behavior
- timeout behavior
- failed-run persistence
- SQLite backup/recovery
- explicit environment switching
- Markdown retrieval quality
- larger context behavior
- longer-running model stability

## Final Assessment

The main risk has shifted.

At the beginning of Phase 1, the primary risk was:

```text
Will the architecture actually work?
```

After Phase 1G, the primary risk is now:

```text
Will the working tracer bullet remain reliable,
safe, understandable, and useful as real knowledge is added?
```

That is the correct next engineering problem.

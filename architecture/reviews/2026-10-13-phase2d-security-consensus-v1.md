# Phase 2D Security Consensus v1 — 2026-10-13

## Decision

**Candidate:** Hiwan AI Phase 2D Hardening v1.1, ZIP SHA-256
`e64e16faac584426544a5ff7161e296c4365396bbcec071908cbe8883d23a220`.

**Scope:** minimal local-first public-project Markdown Q&A CLI; no private family,
financial, or production-agent data access is authorized by this decision.

GPT-6 and Gemini reached agreement on the *repair approach*. Gemini's independent
source review concluded **CODE PASS / RUNTIME VERIFICATION REQUIRED**. Approval
for integration also requires the Mac mini runtime evidence and the existing Git
pre-commit secret-scanning gate. Model agreement alone is not security proof.

## Evidence from Mac mini isolated working-copy validation

- Verified baseline commit: `c202c8cf941e8dc1c6bd2393e8fd2c0abf758ab2`.
- Hardening ZIP SHA-256 matched the reviewed source manifest; all 8 patch files
  matched their expected SHA-256 values.
- **77 Python tests passed** on CPython 3.13.16.
- 21 checked-out Markdown files passed the smoke check: no indexed symlink or
  resolved path outside the checkout; this is not a blanket secret audit.
- Real Ollama/Qwen questions demonstrated: accepted Public Software / Private
  Data policy, all eight SQLite run columns, attribution of Gemini's historical
  governance critique, and rejection of a nonexistent Phase 1 MCP endpoint.
- The original repository HEAD and worktree status were unchanged by the isolated test.
- Private raw evidence remains under `~/.hiwan/dev/logs/` and must not be committed.

## Findings and disposition

| Finding | Disposition |
| --- | --- |
| Mixed-case excluded directories | Fixed; `casefold` directory comparisons and regression tests |
| Hardlinks into the checkout | Mitigated; reject ordinary files with `st_nlink > 1` |
| Policy vs. historical-review authority | Fixed with intent-sensitive ranking and regression tests |
| Short Markdown sections losing nested headings | Fixed; retain nested heading terms |
| Headings inside fenced code blocks | Fixed for covered fence syntax; regression tested |
| Untrusted Markdown and forged evidence labels | Mitigated via system/user separation, JSON data boundary, and citation-ID validation; not eliminated |
| Ollama response timeout | Explicit diagnostic error handling added |
| CJK retrieval and very large Markdown files | Deferred; scalability and multilingual quality follow-up |

## Accepted residual risks and operating restrictions

- A valid `[S1]` label verifies only that the label was allocated. It does not
  prove that a natural-language claim is true or correctly supported. Human
  review remains necessary for important answers.
- Prompt-injection controls reduce risk, but do not eliminate all ways an
  untrusted Markdown excerpt might influence local model output. A dedicated
  adversarial real-Qwen injection run was **not** included in this gate.
- Path, symlink, and hardlink checks are not an OS sandbox and do not establish
  resistance to a malicious local process or file replacement races.
- No blanket secret-content audit of the public Markdown corpus is claimed.
- SQLite `prompt`, `response`, and `tool_result` can contain private material;
  databases and real records remain outside Git at `~/.hiwan/`.
- The CLI must remain scoped to the public project documents; do not grant it
  general read access to private user/family corpora in this phase.

## Gate for main-branch integration

Only after (1) exact reviewed ZIP hash, (2) matching isolated evidence,
(3) main-worktree full tests, (4) real local Qwen CLI answers, (5) Git staged
file allowlist and Gitleaks pass, and (6) normal non-force `git push` may the
Phase 2D commit be treated as published. Failures must stop the script.

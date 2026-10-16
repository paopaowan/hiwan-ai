# Hiwan Learning System

Learning notes are durable engineering knowledge, not disposable chat history. This directory holds **public-safe** notes; private operational evidence and personal/family data remain outside this public repository.

## Daily record template

- **Learned** — knowledge gained
- **Built** — what was actually implemented, versus planned
- **Understood** — causal explanation and trade-offs
- **Failed** — failures and their evidence
- **Gotchas** — practical pitfalls
- **Decisions** — confirmed decisions, distinguished from proposals
- **Questions** — open matters
- **Next** — actionable follow-up
- **Commands** — actual commands and reproducible checks, sanitized before publication

Include the date, relevant commit SHA if verified, whether a change ran only in a local test or was deployed, and which conclusions are inferred rather than directly checked.

## Multi-workstream process

1. **Each development workstream records its own learning** after a meaningful work session.
2. **Dev OS coordinates project-wide index/status updates** and reports unpublished or unbacked-up committed work.
3. **Public documentation is curated** on a regular cadence or at milestones, after review of changed files and repository history for secrets and private data.
4. **Private encrypted backup is separate** from public publication. Verify uploads, then independently test restoration.
5. **Independent architecture reviews** occur for consequential boundary changes, not routine refactors and unit tests.

Never publish secrets, family/child records, real databases, access tokens, account-specific billing details, raw runtime logs, or private source materials merely because they are useful for debugging.

## Notes

- [2026-10-06 — foundation setup](2026-10-06.md) (historical snapshot; later architecture supersedes some early assumptions)
- [2026-10-17 — public retrospective](2026-10-17.md) (summarizes selected October 14–17 lessons; not a reconstructed daily execution log)

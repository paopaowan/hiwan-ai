# Hiwan AI OS

**Personal-first, family-ready, local-first data, cloud-enabled AI.**

Hiwan AI OS is an evolving personal and family AI platform. It aims to make AI useful in daily life while keeping durable user knowledge, private data, identity, and control independent from any particular model or agent vendor.

> **Public documentation snapshot — 2026-10-17.** This public repository is a curated software and learning record, **not** a live production status dashboard. Private local development may be ahead of the public branch. Proposals are not implementations or accepted architecture decisions.

## Three product and engineering domains

### Family Chat

Family-facing chat and personal-knowledge experiences, with a focus on straightforward natural-language interaction and quality of responses. Cloud model inference may be used where appropriate and authorized. Long-term memory and identity must remain independent from individual providers.

The family-facing application has reached an internal feedback phase; this public page makes no production-readiness or deployment-version claim.

### Dev OS

An AI-assisted software development environment intended to reduce manual coding, testing, and deployment preparation. The direction is one coding agent editing an isolated workspace at a time, with reproducible tests and version-specific approval for high-impact actions.

- Codex: first candidate for a primary coding agent.
- Claude Code: prospective fallback, to be considered verified only after completing an equivalent integration and rollback exercise.
- Qwen Code: cross-region alternative to evaluate where applicable.
- Hermes Agent: future research in isolated agent orchestration, not a privileged production operator.

These are development directions, not claims that the agents have been installed or independently validated.

### Admin OS

A separate administration and operations domain for identity, policy, software lifecycle, backups, and recovery. A family-chat request must not imply shell access, administrative rights, or production deployment authority.

## First Dev OS application: Angolan Portuguese learning

A beginner-friendly **pt-AO** learning application intended for work/business and everyday conversations, with an English bridge where useful.

- **MVP-A:** local document intake, offline OCR on macOS, local knowledge storage, 30 business + 30 everyday starter phrases, Markdown notes, translation workflow, vocabulary cards, translation history, and local recording/playback.
- **MVP-B:** source-checked pronunciation audio and slow listening/repetition, with regional accent clearly labeled. Non-Angolan reference audio must never be presented as verified pt-AO speech; automatic accent scoring is not assumed accurate.

User documents, voice recordings, and learning history are private by default. Paid cloud translation or speech services require authorization and cost controls before use.

## Architectural principles

1. **Public software / private data.** Source and non-sensitive documentation may be public; family conversations, personal documents, credentials, local databases, and raw runtime logs do not belong in this repository.
2. **Data and model independence.** Durable memory, knowledge, and application data are distinct from models, agents, and inference runtimes.
3. **Identity -> Policy -> Tool -> Data.** Agents do not receive unrestricted access.
4. **Cloud inference is not cloud ownership of memory.** A provider receives only data appropriate to a specific authorized purpose.
5. **Useful development first.** Isolated coding, local tests, and synthetic-data experimentation should be fast. Spending money, accessing real family data, deploying to active family services, and public releases require their appropriate explicit authorization.
6. **Engineering records are durable.** Learning notes include successful work, failures, pitfalls, and verification evidence.

## Public documentation

- [Roadmap](ROADMAP.md) — current direction and stage boundaries
- [Architecture principles](ARCHITECTURE.md) — original architecture baseline
- [Accepted decisions in the public branch](DECISIONS.md) — not necessarily the latest local project decisions
- [Learning notes](learning/README.md) — how lessons are recorded
- [October 2026 public learning recap](learning/2026-10-17.md) — sanitized lessons and known limitations

## Publication and backup

This repository publishes **reviewed, non-sensitive** software and learning material. Private development and the public branch may move at different speeds.

A separate encrypted offsite Git snapshot was upload-verified in October 2026; a clean-environment recovery test and private runtime-data recovery remain distinct tasks. A Git snapshot does not back up uncommitted work or production databases.

Public releases should be reviewed for privacy and secrets, and should never be used as a substitute for encrypted private backups.

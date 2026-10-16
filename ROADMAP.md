# Hiwan AI OS — Directional Roadmap

**Public progress summary — 2026-10-17.** This roadmap records architectural direction and evidence categories, not an assurance that every listed feature is deployed. The public GitHub main branch may lag behind local development branches.

## North star

Build a personal AI platform that can extend safely to family use, while gradually making AI coding agents capable of doing most routine implementation, testing, and deployment preparation under human direction.

The platform separates **Family Chat**, **Dev OS**, and **Admin OS**. All three rely on local-first data stewardship and explicit identity and policy boundaries.

## Track 1 — Family Chat

**Current direction:** feedback-led improvements after an internal test phase.

- Natural-language chat and personal-knowledge workflows
- Replaceable cloud-model providers with explicit purpose-based data sharing
- Independent user memory and data ownership
- Clear boundaries between family-facing behavior and administrative abilities

**Do not infer:** a universal cloud-provider failover guarantee, production-grade encrypted memory storage, or completed data-governance features solely from this roadmap.

## Track 2 — Dev OS

**Immediate focus:** verify an isolated, terminal-first coding-agent development loop.

1. Inventory the local and remote repository state; preserve and reconcile existing work before further public updates.
2. Prepare an OS-isolated, SSH-compatible development environment; do not rely on a graphical desktop session.
3. Evaluate Codex first using a shared task contract and test evidence.
4. Validate Claude Code as a real backup through equivalent work and an explicit rollback exercise; keep alternative regional tooling under consideration.
5. Later, research Hermes Agent in a separate non-production sandbox.

The isolated practice environment is intended for rapid development with synthetic data. Real family data, paid API calls, deployments to active family services, and public publication remain separately authorized activities.

## Track 3 — First application: Portuguese for Angola (pt-AO)

### MVP-A — local learning workflow

First priority:

**Document scan/import -> offline macOS OCR -> local corpus/knowledge store**

Then:

- A beginner starter pack: **30 business + 30 everyday phrases**
- Markdown learning notes
- Translation workflow with locally saved history
- Flashcards and a simple review experience
- Local self-recording and playback

The learning store is separate from the family-chat memory store. Cloud OCR, translation, transcription, and other paid services are off until the required use-specific consent and spending safeguards are active.

### MVP-B — pronunciation

- Record provenance, speaker/accent, license, and quality evidence for each pronunciation asset.
- Prefer appropriately licensed and validated Angolan Portuguese recordings.
- If a Portuguese-from-Portugal reference is used temporarily, label it as such rather than claiming pt-AO.
- Provide listening, slow playback where faithfully supported, and repeat-after-me practice.
- Do not promise automatic pronunciation scoring without accent-specific validation.

MVP-B is a required part of the full language-learning MVP, but is scheduled separately so that unavailable speech sources do not block MVP-A.

## Track 4 — Admin OS and data stewardship

- Separation of identities, privileges, credentials, and execution environments
- Reviewable, version-pinned deployment approvals
- Private encrypted backups and **tested recovery**
- Privacy-aware memory, provider-specific consent, and spending safeguards
- Eventual automation only after adequate sandboxing and evidence

Admin OS is not equivalent to giving chatbots unrestricted control of the host.

## Governance and publication

- Ordinary coding and testing in an isolated development workspace do not require architecture committee review.
- High-impact privacy, access, deployment, and provider-cost changes require the existing review and authorization process.
- The public repository includes only material suitable for public release.
- The authoritative state of a running system must be checked against its specific local Git SHA, deployed artifact, and test evidence.
- Architecture **PROPOSED** does not mean **ACCEPTED**; a documented target does not mean an implementation is complete.

## Next public documentation milestone

After local changes are reconciled with this public documentation-only update, publish additional sanitized implementation evidence and reviewed code as separate, clearly scoped commits. Preserve original local commit history and private data boundaries.

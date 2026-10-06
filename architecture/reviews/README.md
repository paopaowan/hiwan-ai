# Architecture Reviews

This directory contains independent reviews of architecture proposals.

## Reviewers

```text
reviews/
├── gpt/
├── gemini/
├── claude/
└── other/
```

The directory is organized by reviewer, not by proposal, so each AI can maintain its own review trail.

## Review naming

```text
YYYY-MM-DD-<proposal-slug>--<reviewer>.md
```

## Independence

A reviewer should not read other reviewers' conclusions before producing its initial review when independent validation is desired.

After all independent reviews exist, a reconciliation step may compare them.

## Important

A review is advisory.

Only a decision recorded by Richard in `DECISIONS.md` becomes an accepted architectural decision.

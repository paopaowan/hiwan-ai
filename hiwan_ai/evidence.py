"""Selection of relevant, authoritative evidence for a specific user question.

No blanket rule that DECISIONS.md must be first for every query.
"""
from __future__ import annotations

from dataclasses import dataclass

from .knowledge import SearchHit, query_terms


@dataclass(frozen=True)
class Evidence:
    label: str
    hit: SearchHit

    @property
    def location(self) -> str:
        return self.hit.reference


def question_intent(question: str) -> str:
    terms = set(query_terms(question))
    if terms & {'gemini', 'review', 'critique', 'criticize', 'feedback'}:
        return 'review'
    if terms & {'decision', 'decisions', 'policy', 'boundary',
                'requirement', 'rule', 'rules', 'must', 'should'}:
        return 'policy'
    return 'general'


def _authority(hit: SearchHit, intent: str) -> int:
    path = hit.path
    if intent == 'review':
        if 'gemini' in path.casefold():
            return 3
        return 2 if path.startswith('architecture/reviews/') else 0
    if intent != 'policy':
        return 0
    if path == 'DECISIONS.md':
        return 3
    if path == 'ARCHITECTURE.md':
        return 2
    if path == 'architecture/reviews/2026-10-07-consensus-architecture-v1.md':
        return 2
    if path in {'AGENTS.md', 'AI_CONTEXT.md'}:
        return 1
    return 0


def select_evidence(question: str, candidates: list[SearchHit],
                    *, limit: int = 3) -> list[Evidence]:
    if limit < 1:
        raise ValueError('limit must be >= 1')
    if not candidates:
        return []

    total = max(hit.total_terms for hit in candidates)
    max_score = max(hit.score for hit in candidates)
    # Canonical sources cannot override an unrelated document: there must be
    # substantial term coverage AND at least moderate retrieval relevance.
    qualified = [hit for hit in candidates if (
        hit.matched_terms >= max(1, (total + 1) // 2)
        and hit.score >= 0.4 * max_score
    )]
    if not qualified:
        return []

    intent = question_intent(question)
    if intent == 'general':
        qualified.sort(key=lambda h: (-h.score, -h.matched_terms,
                                      h.path, h.start_line))
    else:
        qualified.sort(key=lambda h: (-_authority(h, intent), -h.score,
                                      -h.matched_terms, h.path, h.start_line))

    # Avoid filling all context slots with adjacent sections of one document.
    selected = []
    per_path: dict[str, int] = {}
    for hit in qualified:
        if per_path.get(hit.path, 0) >= 2:
            continue
        selected.append(Evidence(label=f'S{len(selected) + 1}', hit=hit))
        per_path[hit.path] = per_path.get(hit.path, 0) + 1
        if len(selected) >= limit:
            break
    return selected

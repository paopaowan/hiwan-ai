"""Selection of relevant, authoritative evidence for a specific user question.

No blanket rule that DECISIONS.md must be first for every query.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from .knowledge import SearchHit, query_terms, tokenize

# A concrete filesystem *file* path is more informative than a generic
# persistence statement when the question asks WHERE a file lives.
# Require a final extension so directory paths alone do not take over.
_FILE_LOCATION_RE = re.compile(
    r'(?<![\w/])(?:~/|/)(?:[\w.-]+/)+[\w.-]+\.[a-zA-Z0-9]{1,10}(?![\w.-])'
)
_LOCATION_TERMS = frozenset({'where', 'location', 'located', 'filepath', 'path'})


@dataclass(frozen=True)
class Evidence:
    label: str
    hit: SearchHit

    @property
    def location(self) -> str:
        return self.hit.reference


def question_intent(question: str) -> str:
    terms = set(query_terms(question))
    # Explicit questions *about an author's opinion* are historical reviews,
    # even when the subject is a policy. Review *policy* itself is canonical.
    q = question.casefold()
    asks_reviewer = 'gemini' in terms and any(
        clue in q for clue in ('what did', 'what concern', 'according to',
                              'gemini say', 'gemini state', 'gemini recommend')
    )
    if asks_reviewer:
        return 'review'
    if terms & {'decision', 'decisions', 'policy', 'boundary',
                'requirement', 'rule', 'rules', 'must', 'should',
                'defer', 'deferred', 'postpone', 'postponed',
                'accepted', 'adopted', 'decided'}:
        return 'policy'
    if terms & {'gemini', 'review', 'critique', 'criticize', 'feedback'}:
        return 'review'
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
    if re.fullmatch(r'architecture/reviews/\d{4}-\d{2}-\d{2}-consensus-architecture-v[\w.]+\.md', path):
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

    intent = question_intent(question)
    max_score = max(hit.score for hit in candidates)
    # A coverage threshold based on the *entire* user question rejects valid
    # passages when the wording is conversational, translated, or inflected.
    # Compare against the best *retrieved* coverage instead, and require some
    # meaningful overlap without demanding an impossible 50% of query terms.
    best_coverage = max(hit.matched_terms for hit in candidates)
    minimum_overlap = min(2, best_coverage)
    terms = set(query_terms(question))

    def explicitly_named_review(hit: SearchHit) -> bool:
        return (intent == 'review' and 'gemini' in terms
                and 'gemini' in hit.path.casefold()
                and hit.matched_terms >= 1)

    qualified = [
        hit for hit in candidates
        if hit.score >= 0.30 * max_score
        and (hit.matched_terms >= minimum_overlap
             or explicitly_named_review(hit))
    ]
    if not qualified:
        return []

    def heading_matches(hit: SearchHit) -> int:
        return len(set(tokenize(hit.heading)) & terms)

    if intent == 'general':
        qualified.sort(key=lambda h: (-h.score, -h.matched_terms,
                                      h.path, h.start_line))
    else:
        qualified.sort(key=lambda h: (-_authority(h, intent),
                                      -heading_matches(h), -h.score,
                                      -h.matched_terms, h.path, h.start_line))

    # For a file-location question, reserve ONE slot for a relevant passage
    # with a concrete file path. This is an answer-type check, NOT a filename
    # or project-path hardcode. It does not affect policy or review queries.
    if intent == 'general' and _LOCATION_TERMS.intersection(tokenize(question)):
        path_hits = [
            hit for hit in qualified
            if _FILE_LOCATION_RE.search(hit.snippet) and heading_matches(hit) > 0
        ]
        if path_hits:
            best_path = max(
                path_hits,
                key=lambda hit: (heading_matches(hit), hit.matched_terms,
                                 hit.score, -len(hit.path), -hit.start_line),
            )
            qualified.remove(best_path)
            qualified.insert(0, best_path)

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

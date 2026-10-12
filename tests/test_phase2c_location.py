"""A selected source must carry the answer, not only the right topic."""
from pathlib import Path

from hiwan_ai.evidence import select_evidence
from hiwan_ai.knowledge import MarkdownKnowledgeBase


def _write(root: Path, path: str, text: str) -> None:
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')


def _evidence(root: Path, question: str):
    kb = MarkdownKnowledgeBase(root)
    return select_evidence(question, kb.search(question, limit=20), limit=3)


def test_location_answer_requires_actual_path_in_excerpt(tmp_path: Path) -> None:
    _write(tmp_path, 'architecture.md',
           '# Architecture\n\n## Phase 1 SQLite persistence database\n'
           'SQLite was selected for the Phase 1 database and agent run.\n'
           '## Phase 1 agent run database\n'
           'The Phase 1 agent run database validates local persistence and tests.\n')
    _write(tmp_path, 'learning/phase1.md',
           '# Learning\n\n## Phase 1G agent run SQLite database\n'
           'The agent run persisted and tests passed outside the repository.\n'
           '## Phase 1F SQLite persistence\n'
           'The persistent database file is located at '
           '`~/.hiwan/dev/databases/hiwan.db`.\n')
    q = 'Where is the Phase 1 SQLite agent run database persisted?'
    selected = _evidence(tmp_path, q)
    assert selected and any('~/.hiwan/dev/databases/hiwan.db' in item.hit.snippet
                            for item in selected)
    assert any('Phase 1F' in item.hit.heading for item in selected)


def test_unrelated_file_path_does_not_override_topic(tmp_path: Path) -> None:
    _write(tmp_path, 'README.md',
           '# README\n\n## Repository location\n'
           'A log is saved to `~/.local/logs/unrelated.log`.\n'
           '## SQLite database persistence\n'
           'SQLite stores runs on disk but this file does not specify a path.\n')
    selected = _evidence(tmp_path, 'Where is the SQLite database persisted?')
    assert selected and selected[0].hit.heading == 'SQLite database persistence'


def test_policy_source_authority_unchanged_for_location_question(tmp_path: Path) -> None:
    _write(tmp_path, 'DECISIONS.md',
           '# Decisions\n\n## Decision 011 — Private data boundary\n'
           'Private data must remain physically outside the public repository.\n')
    _write(tmp_path, 'review.md',
           '# Review\n\n## Private data boundary\n'
           'A temporary report is at `~/tmp/output/review.txt`. '
           'The review recommends a private root.\n')
    selected = _evidence(tmp_path, 'Where must private data live relative to the public repository?')
    assert selected and selected[0].hit.path == 'DECISIONS.md'

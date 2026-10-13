"""Relevant evidence must preserve complete short Markdown tables, not cut them in half.

A generic excerpt-budget regression, based on the real Phase 2D SQLite schema
question. Uses synthetic documentation only; no private data or Ollama.
"""
from pathlib import Path

from hiwan_ai.evidence import select_evidence
from hiwan_ai.knowledge import MarkdownKnowledgeBase


FIELDS = (
    'id', 'created_at', 'identity', 'prompt',
    'response', 'tool_used', 'tool_result', 'status',
)


def test_medium_markdown_section_keeps_entire_answer_table(tmp_path: Path) -> None:
    # A 1,000-character excerpt cut the verified schema table midway.
    # The section below mimics a learning journal with contextual material
    # before an eight-field SQLite table. It is longer than the old budget
    # and shorter than the new, bounded budget.
    header = (
        '# 2026-10-13\n\n## Built\n\n'
        '### Knowledge CLI\n\n'
        'Phase 2D validates local Qwen questions with source references.\n\n'
        '### New question evaluation\n\n'
        + ('These checks establish reproducible knowledge retrieval behavior.\n' * 7)
        + '\n### Verified SQLite run record schema\n\n'
        'The Phase 1 SQLite run record persists the following fields:\n\n'
    )
    table = (
        '| Column | Meaning |\n| --- | --- |\n'
        + ''.join(f'| `{name}` | Stored run record value for {name} |\n'
                  for name in FIELDS)
    )
    content = header + table + '\nPrivate data must stay outside Git.\n'
    section = content.split('## Built', 1)[1]
    assert 1000 < len(section) < 2000, len(section)
    (tmp_path / 'learning').mkdir()
    (tmp_path / 'learning' / '2026-10-13.md').write_text(content, encoding='utf-8')

    question = 'What information does the Phase 1 SQLite run record persist?'
    candidates = MarkdownKnowledgeBase(tmp_path).search(question, limit=20)
    chosen = select_evidence(question, candidates, limit=3)
    assert chosen
    excerpt = '\n'.join(item.hit.snippet for item in chosen)
    for field in FIELDS:
        assert f'`{field}`' in excerpt, f'Missing field: {field}'
    assert 'learning/2026-10-13.md:L3-' in chosen[0].location


def test_long_excerpt_stays_bounded_and_focused(tmp_path: Path) -> None:
    (tmp_path / 'README.md').write_text(
        '# Test\n\n## Long\n'
        + ('General unrelated documentation.\n' * 170)
        + 'Special trace persistence content is described here.\n'
        + ('More unrelated documentation.\n' * 100),
        encoding='utf-8',
    )
    hits = MarkdownKnowledgeBase(tmp_path).search('special trace persistence')
    assert hits
    assert 'Special trace persistence content' in hits[0].snippet
    assert len(hits[0].snippet) <= 2010

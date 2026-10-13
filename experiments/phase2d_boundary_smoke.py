"""Read-only Phase 2D.3 check against the actual checkout; no model calls.

This command neither alters source Markdown nor visits ~/.hiwan directly.
"""
from pathlib import Path

from hiwan_ai.knowledge import MarkdownKnowledgeBase


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    kb = MarkdownKnowledgeBase(root)
    docs = kb.discover()
    assert docs, 'FAIL: public Markdown corpus is empty'
    assert any(doc.path == 'DECISIONS.md' for doc in docs), 'FAIL: canonical decisions missing'

    for doc in docs:
        source = root / doc.path
        assert not source.is_symlink(), f'FAIL: symlink indexed: {doc.path}'
        assert source.resolve().is_relative_to(root), f'FAIL: escaped repo: {doc.path}'

    note = root / 'learning' / '2026-10-13.md'
    if note.is_file():
        lookup = kb.search('agent_runs created_at tool_result')
        assert any(hit.path == 'learning/2026-10-13.md' for hit in lookup), (
            'FAIL: latest learning note not available for search'
        )
        print('PASS: 2026-10-13 SQLite knowledge is searchable')
    else:
        print('NOTE: 2026-10-13 learning note not present; optional check skipped')

    print(f'PASS: {len(docs)} Markdown files indexed inside checkout')
    print('PASS: no indexed file is a symlink or resolves outside the checkout')
    print('NOTE: This checks filesystem scope, not whether every public Markdown is free of secrets.')


if __name__ == '__main__':
    main()

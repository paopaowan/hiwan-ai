"""Phase 2D.3: dynamic Markdown and filesystem boundary regressions.

All content is synthetic and lives in pytest temporary directories.
No Ollama call, database connection, or access to ~/.hiwan is required.
"""
from pathlib import Path

import pytest

from hiwan_ai import cli
from hiwan_ai.knowledge import MarkdownKnowledgeBase


def test_added_markdown_is_visible_without_restarting_index(tmp_path: Path) -> None:
    kb = MarkdownKnowledgeBase(tmp_path)
    assert not kb.search('cobaltknowledgeflag')
    document = tmp_path / 'new-note.md'
    document.write_text('# New Note\n\n## Details\n\ncobaltknowledgeflag is present.\n', encoding='utf-8')
    hits = kb.search('cobaltknowledgeflag')
    assert hits and hits[0].path == 'new-note.md'
    assert 'cobaltknowledgeflag' in hits[0].snippet


def test_markdown_edits_and_deletion_are_visible_without_restarting(tmp_path: Path) -> None:
    document = tmp_path / 'note.md'
    kb = MarkdownKnowledgeBase(tmp_path)
    document.write_text('# Note\n\n## Topic\n\ncrimsonknowledgeflag\n', encoding='utf-8')
    assert kb.search('crimsonknowledgeflag')
    document.write_text('# Note\n\n## Topic\n\nindigoknowledgeflag\n', encoding='utf-8')
    assert not kb.search('crimsonknowledgeflag')
    assert kb.search('indigoknowledgeflag')
    document.unlink()
    assert not kb.search('indigoknowledgeflag')


def test_reference_line_range_tracks_inserted_lines(tmp_path: Path) -> None:
    p = tmp_path / 'architecture.md'
    original = '# Design\n\n## Separate Layer\n\nzephyrlineanchor: boundary.\n'
    p.write_text(original, encoding='utf-8')
    kb = MarkdownKnowledgeBase(tmp_path)
    first = kb.search('zephyrlineanchor')[0]
    assert first.start_line == 3
    assert first.end_line == 5
    assert first.reference == 'architecture.md:L3-L5'
    p.write_text('# Design\n\n' + 'Added context.\n' * 7 + '\n' + original[10:], encoding='utf-8')
    second = kb.search('zephyrlineanchor')[0]
    assert second.start_line == first.start_line + 8
    assert second.end_line == first.end_line + 8
    assert 'zephyrlineanchor' in second.snippet
    source_lines = p.read_text(encoding='utf-8').splitlines()
    assert 'zephyrlineanchor' in '\n'.join(source_lines[second.start_line-1:second.end_line])


def test_excluded_directory_files_are_not_read_or_retrieved(tmp_path: Path) -> None:
    exclusions = ('.git', '.venv', '.hiwan', 'private', 'memory', 'secrets',
                  'credentials', 'node_modules', '__pycache__')
    for name in exclusions:
        folder = tmp_path / name
        folder.mkdir()
        (folder / 'test.md').write_text('# Sensitive\n\nsyntheticprivacytoken\n', encoding='utf-8')
    (tmp_path / 'safe.md').write_text('# Public\n\npublicboundarytoken\n', encoding='utf-8')
    kb = MarkdownKnowledgeBase(tmp_path)
    assert [doc.path for doc in kb.discover()] == ['safe.md']
    assert not kb.search('syntheticprivacytoken')
    assert kb.search('publicboundarytoken')[0].path == 'safe.md'


def test_external_markdown_file_symlink_not_indexed(tmp_path: Path) -> None:
    root = tmp_path / 'repo'
    external = tmp_path / 'outside'
    root.mkdir()
    external.mkdir()
    outside = external / 'private-note.md'
    outside.write_text('# Private\n\nforbiddenfiletoken\n', encoding='utf-8')
    try:
        (root / 'linked.md').symlink_to(outside)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f'symlinks unsupported: {exc}')
    kb = MarkdownKnowledgeBase(root)
    assert not kb.discover()
    assert not kb.search('forbiddenfiletoken')


def test_external_directory_symlink_not_traversed(tmp_path: Path) -> None:
    root = tmp_path / 'repo'
    external = tmp_path / 'outside'
    root.mkdir()
    external.mkdir()
    (external / 'private-note.md').write_text('# Private\n\nforbiddenfoldertoken\n', encoding='utf-8')
    try:
        (root / 'linked-folder').symlink_to(external, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f'symlinks unsupported: {exc}')
    kb = MarkdownKnowledgeBase(root)
    assert not kb.discover()
    assert not kb.search('forbiddenfoldertoken')


def test_cli_rejects_arbitrary_private_knowledge_root(monkeypatch, capsys) -> None:
    # This is an interface regression: the public-project CLI must not gain
    # a --root option that casually targets private data.
    monkeypatch.setattr(cli, 'build_agent', lambda _: pytest.fail('agent should not be built'))
    with pytest.raises(SystemExit) as exc:
        cli.main(['ask', 'hello', '--root', '/tmp/private'])
    assert exc.value.code == 2
    assert 'unrecognized arguments' in capsys.readouterr().err

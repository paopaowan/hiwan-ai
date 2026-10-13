"""Independent-review regressions: sandbox-only Markdown and evidence selection."""
from pathlib import Path
import os

import pytest

from hiwan_ai.evidence import question_intent, select_evidence
from hiwan_ai.knowledge import MarkdownKnowledgeBase


def _write(root: Path, relative: str, text: str) -> Path:
    p = root / relative
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    return p


@pytest.mark.parametrize('folder', ['Private', 'SECRETS', '.Hiwan', 'MeMoRy', 'Credentials'])
def test_mixed_case_sensitive_directories_are_excluded(tmp_path: Path, folder: str) -> None:
    _write(tmp_path, f'{folder}/secret.md', '# Secret\n\nhiddenprivatetoken')
    _write(tmp_path, 'public.md', '# Public\n\nvisiblepublictoken')
    kb = MarkdownKnowledgeBase(tmp_path)
    assert [doc.path for doc in kb.discover()] == ['public.md']
    assert kb.search('hiddenprivatetoken') == []


def test_user_supplied_exclusion_casefolds(tmp_path: Path) -> None:
    _write(tmp_path, 'ConFiDenTial/one.md', '# Confidential\n\nsecretmark123')
    assert not MarkdownKnowledgeBase(tmp_path, excluded_dirs={'confidential'}).discover()


def test_hardlink_from_outside_checkout_not_read(tmp_path: Path) -> None:
    root = tmp_path / 'repo'
    root.mkdir()
    outside = _write(tmp_path, 'private/important.md', '# Private\n\nhardlinkprivatetoken')
    try:
        os.link(outside, root / 'innocent.md')
    except OSError as exc:
        pytest.skip(f'hard links unsupported here: {exc}')
    kb = MarkdownKnowledgeBase(root)
    assert 'innocent.md' not in [d.path for d in kb.discover()]
    assert kb.search('hardlinkprivatetoken') == []


@pytest.mark.parametrize('fence', ['```bash', '~~~~python'])
def test_fenced_comments_never_become_section_headings(tmp_path: Path, fence: str) -> None:
    close = fence[0] * (4 if fence[0] == '~' else 3)
    _write(tmp_path, 'notes.md',
           '# Real Title\n\n## Real Section\n' + fence + '\n'
           '## Fake Chapter\n# Fake Document Title\n' + close + '\n'
           'Actual verified entry is greenleafmarker.\n')
    kb = MarkdownKnowledgeBase(tmp_path)
    assert kb.discover()[0].title == 'Real Title'
    hits = kb.search('greenleafmarker')
    assert hits and hits[0].heading == 'Real Section'
    assert hits[0].start_line == 3


def test_no_real_h1_ignores_code_comment_as_document_title(tmp_path: Path) -> None:
    _write(tmp_path, 'untitled.md', '```bash\n# fake title\n```\n\n## Detail\nupdatemark\n')
    assert MarkdownKnowledgeBase(tmp_path).discover()[0].title == 'untitled'


def test_short_subsection_titles_participate_in_search(tmp_path: Path) -> None:
    _write(tmp_path, 'learning.md', '# Note\n\n## Built\nGeneral introduction.\n'
           '### Verified SQLite schema\nThe stored values are listed below.\n')
    hits = MarkdownKnowledgeBase(tmp_path).search('verified sqlite schema')
    assert hits and 'Verified SQLite schema' in hits[0].heading
    assert hits[0].start_line == 3


def test_formal_review_policy_does_not_get_historical_review_authority(tmp_path: Path) -> None:
    _write(tmp_path, 'DECISIONS.md', '# Decisions\n\n## Decision 008 — Independent Review Policy\n'
           'Accepted policy defines independent review and approved proposals.\n')
    _write(tmp_path, 'architecture/reviews/gemini/historical.md',
           '# Gemini Review\n\n## Review Policy\n'
           'A historical reviewer discusses review policy.\n')
    q = 'What is the accepted decision on independent review policy?'
    assert question_intent(q) == 'policy'
    selected = select_evidence(q, MarkdownKnowledgeBase(tmp_path).search(q, limit=20))
    assert selected and selected[0].hit.path == 'DECISIONS.md'


def test_named_gemini_opinion_remains_historical_review(tmp_path: Path) -> None:
    _write(tmp_path, 'DECISIONS.md', '# Decisions\n\n## Privacy Boundary\nAccepted policy boundary.\n')
    _write(tmp_path, 'architecture/reviews/gemini/historical.md',
           '# Gemini Review\n\n## Privacy Boundary\nGemini said boundary should be physical.\n')
    q = 'What did Gemini say about the privacy boundary?'
    assert question_intent(q) == 'review'
    selected = select_evidence(q, MarkdownKnowledgeBase(tmp_path).search(q, limit=20))
    assert selected and 'gemini' in selected[0].hit.path


def test_new_consensus_review_version_not_hardcoded(tmp_path: Path) -> None:
    _write(tmp_path, 'architecture/reviews/2026-10-13-consensus-architecture-v2.md',
           '# New Consensus\n\n## Boundary Policy\nAccepted policy boundary rule.\n')
    _write(tmp_path, 'architecture/reviews/other-review.md',
           '# Review\n\n## Boundary Policy\nAccepted policy boundary rule.\n')
    q = 'What is the policy boundary?'
    selected = select_evidence(q, MarkdownKnowledgeBase(tmp_path).search(q, limit=20))
    assert selected
    assert selected[0].hit.path.endswith('consensus-architecture-v2.md')

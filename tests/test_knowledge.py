from pathlib import Path

import pytest

from hiwan_ai.knowledge import MarkdownKnowledgeBase


def test_discover_markdown_and_extract_title(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Root Title\n\nPublic software lives here.\n",
        encoding="utf-8",
    )
    nested = tmp_path / "architecture"
    nested.mkdir()
    (nested / "DECISIONS.md").write_text(
        "# Decisions\n\nPrivate data stays outside Git.\n",
        encoding="utf-8",
    )

    kb = MarkdownKnowledgeBase(tmp_path)
    docs = kb.discover()

    assert [doc.path for doc in docs] == [
        "README.md",
        "architecture/DECISIONS.md",
    ]
    assert docs[0].title == "Root Title"
    assert docs[1].title == "Decisions"


def test_normalized_phrase_ignores_punctuation(tmp_path: Path) -> None:
    (tmp_path / "DECISIONS.md").write_text(
        "# Architecture Decisions\n\n"
        "## Public Software / Private Data Boundary\n\n"
        "Private runtime data must stay outside Git.\n",
        encoding="utf-8",
    )

    kb = MarkdownKnowledgeBase(tmp_path)
    hits = kb.search("Public Software Private Data")

    assert hits
    assert hits[0].path == "DECISIONS.md"
    assert hits[0].matched_terms == 4
    assert hits[0].total_terms == 4


def test_question_stopwords_do_not_distort_ranking(tmp_path: Path) -> None:
    (tmp_path / "DECISIONS.md").write_text(
        "# Architecture Decisions\n\n"
        "## Public Software / Private Data Boundary\n\n"
        "The public repository is ~/hiwan-ai.\n\n"
        "Private runtime data is physically outside Git at ~/.hiwan.\n",
        encoding="utf-8",
    )

    reviews = tmp_path / "architecture" / "reviews"
    reviews.mkdir(parents=True)
    (reviews / "review.md").write_text(
        "# Hiwan AI Review\n\n"
        "What is in Hiwan AI and what is the project about?\n\n"
        "Public software and private data are discussed here.\n",
        encoding="utf-8",
    )

    kb = MarkdownKnowledgeBase(tmp_path)
    hits = kb.search(
        "What is the Public Software Private Data boundary in Hiwan AI?"
    )

    assert hits[0].path == "DECISIONS.md"


def test_best_snippet_starts_near_relevant_section(tmp_path: Path) -> None:
    (tmp_path / "DECISIONS.md").write_text(
        "# Architecture Decisions\n\n"
        "## Decision 001 — Other Topic\n\n"
        "Public APIs can exist for unrelated reasons.\n\n"
        "## Decision 010 — Public Software / Private Data Boundary\n\n"
        "Private runtime data must be physically separated from the public Git repository.\n\n"
        "The public repository is ~/hiwan-ai and private runtime data is under ~/.hiwan.\n",
        encoding="utf-8",
    )

    kb = MarkdownKnowledgeBase(tmp_path)
    hit = kb.search("Public Software Private Data boundary")[0]

    assert "Decision 010" in hit.snippet
    assert "~/.hiwan" in hit.snippet


def test_canonical_decisions_outranks_review_for_same_topic(tmp_path: Path) -> None:
    (tmp_path / "DECISIONS.md").write_text(
        "# Architecture Decisions\n\n"
        "Public Software / Private Data Boundary.\n",
        encoding="utf-8",
    )

    reviews = tmp_path / "architecture" / "reviews"
    reviews.mkdir(parents=True)
    (reviews / "external-review.md").write_text(
        "# External Review\n\n"
        "Public Software Private Data Boundary.\n",
        encoding="utf-8",
    )

    kb = MarkdownKnowledgeBase(tmp_path)
    hits = kb.search("Public Software Private Data")

    assert len(hits) == 2
    assert hits[0].path == "DECISIONS.md"


def test_discovery_skips_excluded_directories(tmp_path: Path) -> None:
    (tmp_path / "visible.md").write_text("# Visible\n", encoding="utf-8")
    hidden = tmp_path / ".git"
    hidden.mkdir()
    (hidden / "hidden.md").write_text("# Hidden\n", encoding="utf-8")

    kb = MarkdownKnowledgeBase(tmp_path)
    docs = kb.discover()

    assert [doc.path for doc in docs] == ["visible.md"]


def test_search_rejects_empty_query(tmp_path: Path) -> None:
    kb = MarkdownKnowledgeBase(tmp_path)

    with pytest.raises(ValueError):
        kb.search("   ")


def test_search_rejects_invalid_limit(tmp_path: Path) -> None:
    kb = MarkdownKnowledgeBase(tmp_path)

    with pytest.raises(ValueError):
        kb.search("hello", limit=0)

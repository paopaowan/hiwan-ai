"""Regression tests for Phase 2C's three missed evidence selections.

All fixtures are synthetic; no Ollama call or personal data is required.
"""
from pathlib import Path

from hiwan_ai.evidence import question_intent, select_evidence
from hiwan_ai.knowledge import MarkdownKnowledgeBase


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _select(root: Path, question: str):
    kb = MarkdownKnowledgeBase(root)
    return select_evidence(question, kb.search(question, limit=20), limit=3)


def test_deferred_mcp_question_selects_accepted_decision(tmp_path: Path) -> None:
    _write(
        tmp_path, "DECISIONS.md",
        "# Decisions\n\n"
        "## Decision 010 — Public Software Private Data\n"
        "Identity Policy Tool Data boundaries are important.\n\n"
        "## Decision 013 — Tool / MCP Separation\n"
        "Tool is an independent abstraction and MCP is an adapter.\n"
        "We deferred a complete MCP server for the first agent.\n\n"
        "### Rationale\n"
        "Avoid protocol lock-in while keeping simple local tools.\n",
    )
    _write(
        tmp_path,
        "architecture/reviews/external.md",
        "# Review\n\n## Discussion\n"
        "Keeping tools simple is important while developing. " * 10,
    )
    q = "Why was MCP deferred while keeping Tool as a separate abstraction?"
    selected = _select(tmp_path, q)
    assert question_intent(q) == "policy"
    assert selected and selected[0].hit.path == "DECISIONS.md"
    assert "Decision 013" in selected[0].hit.heading
    assert "Avoid protocol lock-in" in selected[0].hit.snippet


def test_long_lexical_grounding_question_is_not_filtered_out(tmp_path: Path) -> None:
    _write(
        tmp_path, "learning/2026-10-12.md",
        "# 2026-10-12\n\n## Failed\n"
        "Lexical ranking over-weighted reviews. "
        "Grounding tests exposed incorrect .gitignore claims.\n",
    )
    q = "What went wrong in Phase 2A and Phase 2B lexical ranking and grounding tests?"
    selected = _select(tmp_path, q)
    assert selected
    assert selected[0].hit.path == "learning/2026-10-12.md"
    assert "Failed" in selected[0].hit.heading


def test_explicit_gemini_historical_query_keeps_its_review(tmp_path: Path) -> None:
    _write(
        tmp_path, "architecture/reviews/gemini/review.md",
        "# Gemini Review\n\n"
        "## Solo-development concerns\n"
        "治理流程过重会降低个人开发者效率。 "
        "Review governance overhead only for high-impact changes.\n",
    )
    _write(
        tmp_path, "DECISIONS.md",
        "# Decisions\n\n## Decision 012 — Architecture Governance Threshold\n"
        "Solo developer governance overhead should be limited.\n",
    )
    q = "What did Gemini say about governance overhead for a solo developer?"
    selected = _select(tmp_path, q)
    assert question_intent(q) == "review"
    assert selected and "gemini" in selected[0].hit.path


def test_unrelated_formal_decision_does_not_beat_matching_content(tmp_path: Path) -> None:
    _write(tmp_path, "DECISIONS.md", "# Decisions\n\nFinance planning and budgets.\n")
    _write(tmp_path, "README.md", "# Readme\n\nSourdough fermentation requires yeast.\n")
    selected = _select(tmp_path, "How does sourdough fermentation work?")
    assert selected and selected[0].hit.path == "README.md"


def test_short_decision_keeps_rationale_together(tmp_path: Path) -> None:
    _write(
        tmp_path, "DECISIONS.md",
        "# Decisions\n\n## Decision 013 — Tool / MCP Separation\n"
        "We deferred an MCP server. Tool is the interface.\n\n"
        "### Rationale\n"
        "This avoids protocol lock-in and keeps local development simple.\n",
    )
    hit = MarkdownKnowledgeBase(tmp_path).search("MCP Tool separation", limit=3)[0]
    assert "Decision 013" in hit.heading
    assert "Rationale" in hit.snippet
    assert "protocol lock-in" in hit.snippet


def test_nested_oversized_sections_have_bounded_spans(tmp_path: Path) -> None:
    long_intro = "\n".join(f"Development note {i}: unrelated details." for i in range(180))
    _write(
        tmp_path, "learning/2026-10-07.md",
        "# Day\n\n## Built\n" + long_intro + "\n\n"
        "### Phase 1G — End-to-End Tracer Bullet\n"
        "Agent, Tool, Qwen, and SQLite were integrated and verified.\n",
    )
    hits = MarkdownKnowledgeBase(tmp_path).search("Phase 1G Qwen SQLite")
    assert hits
    assert all(hit.end_line - hit.start_line + 1 <= 90 for hit in hits)
    assert any("Built" in hit.heading and "Phase 1G" in hit.heading for hit in hits)
    assert any("Qwen" in hit.snippet and "SQLite" in hit.snippet for hit in hits)


def test_headingless_long_review_uses_focused_exact_text(tmp_path: Path) -> None:
    lines = ["# Gemini Review"]
    lines.extend("General observations about the system and implementation." for _ in range(280))
    lines.append("Governance overhead for a solo developer should be kept low.")
    lines.extend("Other architectural remarks." for _ in range(60))
    _write(
        tmp_path, "architecture/reviews/gemini/review.md", "\n".join(lines),
    )
    q = "What did Gemini say about governance overhead for a solo developer?"
    evidence = _select(tmp_path, q)
    assert evidence
    assert "gemini" in evidence[0].hit.path
    assert "Governance overhead" in evidence[0].hit.snippet
    assert evidence[0].hit.end_line - evidence[0].hit.start_line + 1 <= 90
    assert evidence[0].location.endswith(
        f"L{evidence[0].hit.start_line}-L{evidence[0].hit.end_line}"
    )


def test_empty_or_unrelated_corpus_returns_no_evidence(tmp_path: Path) -> None:
    _write(tmp_path, "README.md", "# README\n\nSimple local architecture notes.\n")
    assert _select(tmp_path, "quantum chromodynamics") == []


def test_symlink_is_not_followed(tmp_path: Path) -> None:
    outside = tmp_path.parent / (tmp_path.name + "_outside.md")
    outside.write_text("SECRET: outside file", encoding="utf-8")
    try:
        (tmp_path / "linked.md").symlink_to(outside)
        assert [d.path for d in MarkdownKnowledgeBase(tmp_path).discover()] == []
    finally:
        outside.unlink(missing_ok=True)

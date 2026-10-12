from pathlib import Path

from experiments.phase2c_answer_eval import (
    mechanical_checks, markdown_review, write_private_reports,
)


def test_mechanical_checks_do_not_claim_semantic_correctness():
    data = mechanical_checks(
        "Text supported by [S1], but this might still be misleading.",
        [{"label": "S1", "path": "DECISIONS.md"}],
        ["DECISIONS.md"],
    )
    assert data["answer_nonempty"] is True
    assert data["expected_source_selected"] is True
    assert data["has_citation_marker"] is True
    assert data["unknown_citation_labels"] == []
    assert "semantic_pass" not in data


def test_unknown_citation_marked_as_invalid():
    data = mechanical_checks("Claim [S99]", [{"label": "S1", "path": "DECISIONS.md"}], ["DECISIONS.md"])
    assert data["unknown_citation_labels"] == ["[S99]"]


def test_private_reports_and_review_checkboxes(tmp_path: Path):
    report = {
        "run_id": "phase2c-test-run",
        "model": "fake",
        "cases": [{
            "id": "P2C-01", "category": "decision", "question": "What is the boundary?",
            "execution": "ANSWERED", "error": None,
            "answer": "Physical separation [S1]",
            "evidence": [{"label": "S1", "reference": "DECISIONS.md:L1-L15", "heading": "Decision 010"}],
            "mechanical_checks": {"expected_source_selected": True, "has_citation_marker": True,
                                  "unknown_citation_labels": []},
            "review_guide": ["Distinguish primary and secondary safeguards."],
        }],
    }
    json_path, md_path = write_private_reports(report, tmp_path)
    assert json_path.exists() and md_path.exists()
    text = markdown_review(report)
    assert "- [ ] Distinguish primary and secondary safeguards." in text
    assert "Human verdict" in text
    assert (json_path.stat().st_mode & 0o077) == 0
    assert (md_path.stat().st_mode & 0o077) == 0

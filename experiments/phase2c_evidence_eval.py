"""Read-only Phase 2C evidence-selection baseline on actual project questions.

Measures source@3 and section@3, not answer correctness. No LLM calls and
no changes to knowledge/evidence implementation. Report is stored outside Git.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

# A source path alone is too weak to validate retrieval: relevant section matters.
# Each case accepts one or more path+heading pairs. Use 'in' match on heading.
TARGETS: dict[str, tuple[tuple[str, str], ...]] = {
    "P2C-01": (("DECISIONS.md", "Decision 010"),
                 ("ARCHITECTURE.md", "Public Software / Private Data")),
    "P2C-02": (("DECISIONS.md", "Decision 011"),
                 ("architecture/reviews/2026-10-07-consensus-architecture-v1.md", "Private Data Boundary")),
    "P2C-03": (("DECISIONS.md", "Decision 011"),
                 ("learning/2026-10-07.md", "Gotchas")),
    "P2C-04": (("architecture/reviews/gemini/2026-10-07-architecture-review-v1.md", ""),),
    "P2C-05": (("DECISIONS.md", "Decision 013"),
                 ("architecture/reviews/2026-10-07-consensus-architecture-v1.md", "Tool")),
    "P2C-06": (("DECISIONS.md", "Decision 003"),
                 ("architecture/reviews/2026-10-07-consensus-architecture-v1.md", "Identity / Policy"),
                 ("ARCHITECTURE.md", "Core Architectural Boundaries")),
    "P2C-07": (("learning/2026-10-07.md", "Failed"),
                 ("architecture/reviews/2026-10-07-phase1-implementation-review.md", "Important Evidence Against")),
    "P2C-08": (("learning/2026-10-07.md", "Failed"),),
    "P2C-09": (("learning/2026-10-07.md", "Built"),
                 ("architecture/reviews/2026-10-07-phase1-implementation-review.md", "Verified Implementation Evidence")),
    "P2C-10": (("learning/2026-10-07.md", "Built"),
                 ("architecture/reviews/2026-10-07-phase1-implementation-review.md", "Verified Implementation Evidence")),
    "P2C-11": (("learning/2026-10-12.md", "Failed"),),
    "P2C-12": (("architecture/reviews/gemini/2026-10-07-architecture-review-v1.md", ""),),
}


def is_target(hit: object, targets: tuple[tuple[str, str], ...]) -> bool:
    path = str(getattr(hit, "path", ""))
    heading = str(getattr(hit, "heading", ""))
    return any(path == target_path and required_heading.casefold() in heading.casefold()
               for target_path, required_heading in targets)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.home() / "hiwan-ai")
    parser.add_argument("--out", type=Path,
                        default=Path.home() / ".hiwan/dev/logs/phase2c-evidence-baseline.json")
    args = parser.parse_args()

    repo = args.repo.expanduser().resolve()
    sys.path.insert(0, str(repo))
    from hiwan_ai.knowledge import MarkdownKnowledgeBase
    from hiwan_ai.evidence import question_intent, select_evidence

    cases = json.loads((repo / "experiments/phase2c_cases.json").read_text(encoding="utf-8"))
    if {str(case["id"]) for case in cases} != set(TARGETS):
        raise RuntimeError("Evaluation case IDs differ from curated section targets; review rubric before running")

    kb = MarkdownKnowledgeBase(repo)
    results = []
    print("========== PHASE 2C EVIDENCE-SELECTION BASELINE ==========")
    print("Cases:", len(cases))
    print("No LLM calls. Results are diagnostics, not acceptance decisions.")

    for case in cases:
        question = str(case["question"])
        candidate_hits = kb.search(question, limit=20)
        selected = select_evidence(question, list(candidate_hits), limit=3)
        target_pairs = TARGETS[case["id"]]
        source_paths = {path for path, _ in target_pairs}
        source_at_3 = any(ev.hit.path in source_paths for ev in selected)
        section_at_3 = any(is_target(ev.hit, target_pairs) for ev in selected)
        warnings = []
        for ev in selected:
            line_span = max(0, ev.hit.end_line - ev.hit.start_line + 1)
            if line_span > 120:
                warnings.append(f"{ev.label}: section spans {line_span} lines; short snippet may omit the queried detail")
        details = [
            {
                "label": ev.label,
                "path": ev.hit.path,
                "heading": ev.hit.heading,
                "start_line": ev.hit.start_line,
                "end_line": ev.hit.end_line,
                "reference": ev.location,
                "score": ev.hit.score,
                "matched_terms": ev.hit.matched_terms,
                "total_terms": ev.hit.total_terms,
                "snippet_chars": len(ev.hit.snippet),
                "matches_curated_section": is_target(ev.hit, target_pairs),
            }
            for ev in selected
        ]
        results.append({
            "id": case["id"], "question": question, "category": case["category"],
            "inferred_intent": question_intent(question),
            "target_sections": [{"path": p, "heading_contains": h} for p, h in target_pairs],
            "source_in_evidence_at_3": source_at_3,
            "target_section_in_evidence_at_3": section_at_3,
            "selected_evidence": details, "warnings": warnings,
        })
        print(f"\n{case['id']} | source@3={'YES' if source_at_3 else 'NO'} | "
              f"section@3={'YES' if section_at_3 else 'NO'} | intent={question_intent(question)}")
        print("Question:", question)
        for item in details:
            mark = "TARGET" if item["matches_curated_section"] else "other"
            print(f"  [{item['label']}] {item['reference']} | {item['heading']} | {mark}")
        for warning in warnings:
            print("  WARNING:", warning)

    source_count = sum(bool(r["source_in_evidence_at_3"]) for r in results)
    section_count = sum(bool(r["target_section_in_evidence_at_3"]) for r in results)
    print("\n========== SUMMARY ==========")
    print(f"Expected source in selected evidence @3: {source_count}/{len(results)}")
    print(f"Expected section in selected evidence @3: {section_count}/{len(results)}")
    print("Interpretation: diagnostics only; not answer accuracy or release criteria.")
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": str(repo),
        "description": "Evidence source@3 and targeted section@3; no model-generated answers evaluated",
        "total": len(results),
        "source_at_3": source_count,
        "section_at_3": section_count,
        "cases": results,
    }
    out = args.out.expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out.chmod(0o600)
    print("Private report:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

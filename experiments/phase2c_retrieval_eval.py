"""Phase 2C: observational retrieval baseline on real project questions.

Only reads Markdown and the existing Knowledge Layer. Does not call an LLM,
modify project code, or add files inside the Git working tree.

The check is candidate recall@5 against manually named plausible sources;
it is NOT a truth/authority/grounding score and is not a release gate.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


def get_path(hit: object) -> str:
    """Extract a source path across small changes in the SearchHit API."""
    for field in ("path", "source_path", "relative_path", "document_path"):
        value = getattr(hit, field, None)
        if isinstance(value, (str, Path)) and str(value):
            return str(value)
    document = getattr(hit, "document", None)
    if document is not None:
        value = getattr(document, "path", None)
        if isinstance(value, (str, Path)):
            return str(value)
    if isinstance(hit, dict):
        for field in ("path", "source_path", "relative_path", "document_path"):
            if hit.get(field):
                return str(hit[field])
    raise TypeError(f"Cannot identify source path on retrieval result of type {type(hit).__name__}")


def get_metadata(hit: object) -> dict[str, object]:
    result = {}
    for field in ("score", "title", "heading", "start_line", "end_line", "line_start", "line_end"):
        value = getattr(hit, field, None)
        if isinstance(value, (str, int, float)):
            result[field] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.home() / "hiwan-ai")
    parser.add_argument("--out", type=Path, default=Path.home() / ".hiwan/dev/logs/phase2c-retrieval-baseline.json")
    args = parser.parse_args()

    repo = args.repo.expanduser().resolve()
    cases_path = repo / "experiments/phase2c_cases.json"
    if not cases_path.is_file():
        raise SystemExit(f"Missing evaluation cases: {cases_path}")

    sys.path.insert(0, str(repo))
    from hiwan_ai.knowledge import MarkdownKnowledgeBase

    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    if len(cases) < 10:
        raise SystemExit("Expected at least ten evaluation cases")
    kb = MarkdownKnowledgeBase(repo)
    results: list[dict[str, object]] = []

    print("========== PHASE 2C RETRIEVAL BASELINE ==========")
    print("Knowledge root:", repo)
    print("Cases:", len(cases))
    print("No LLM calls; no private-data root accessed intentionally.")

    for case in cases:
        question = str(case["question"])
        try:
            hits = kb.search(question, limit=20)
        except TypeError as exc:
            # Fail transparently if the API changed. Do not hide programming errors.
            raise RuntimeError(
                "Current MarkdownKnowledgeBase.search API differs from the baseline script. "
                "Please share its signature before modifying existing project code."
            ) from exc

        top5 = []
        for hit in list(hits)[:5]:
            item = {"path": get_path(hit)}
            item.update(get_metadata(hit))
            top5.append(item)

        expected = [str(p) for p in case["expected_any"]]
        match = next((p for p in expected if p in [h["path"] for h in top5]), None)
        ok = match is not None
        results.append({
            "id": case["id"],
            "category": case["category"],
            "question": question,
            "expected_any": expected,
            "candidate_source_found_at_5": ok,
            "matched_expected_source": match,
            "top5": top5,
        })
        print(f"\n{case['id']} | {'CANDIDATE FOUND' if ok else 'REVIEW'} | {case['category']}")
        print("Question:", question)
        print("Expected any:", ", ".join(expected))
        for rank, hit in enumerate(top5, 1):
            desc = ", ".join(f"{k}={v}" for k, v in hit.items() if k != "path")
            print(f"  {rank}. {hit['path']}" + (f" ({desc})" if desc else ""))

    found = sum(bool(row["candidate_source_found_at_5"]) for row in results)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": str(repo),
        "metric_description": "Plausible expected source present among top-5 raw candidate results; NOT a grounded-answer accuracy score",
        "total_cases": len(cases),
        "candidate_found_at_5": found,
        "candidate_not_found_at_5": len(cases) - found,
        "cases": results,
    }

    output = args.out.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output.chmod(0o600)

    print("\n========== SUMMARY ==========")
    print(f"Candidate source in top-5: {found}/{len(cases)}")
    print(f"Review cases: {len(cases) - found}")
    print("Report:", output)
    print("This is diagnostic evidence, NOT a Phase 2C acceptance decision.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

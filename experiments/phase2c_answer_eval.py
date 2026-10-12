"""Phase 2C: collect real local-LLM answers for human grounding review.

- Uses the current KnowledgeAgent, Markdown corpus, and Ollama model.
- Does not change ranking or selection algorithms.
- Mechanical checks do NOT certify semantic accuracy or factual grounding.
- Keeps full answers and evidence in ~/.hiwan/dev/logs, outside Git.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
from typing import Any


# Checks are review prompts, NOT automated criteria for accepting an answer.
REVIEW_GUIDE: dict[str, tuple[str, ...]] = {
    "P2C-01": (
        "Public source code may be shared; private personal/family data stays outside the Git working tree.",
        "Do not confuse .gitignore with physical data separation.",
    ),
    "P2C-02": (
        "Identify ~/.hiwan/ (with development data under ~/.hiwan/dev/) as outside ~/hiwan-ai/.",
        "Distinguish physical storage location from Git ignore rules.",
    ),
    "P2C-03": (
        "Explain that .gitignore is defense-in-depth, not the primary privacy boundary.",
        "Explain the accidental git-add / configuration risk of relying on .gitignore alone.",
    ),
    "P2C-04": (
        "Attribute the criticism to Gemini's review, not to the formal project decision.",
        "Mention accidental publication if private data exists inside the repository.",
    ),
    "P2C-05": (
        "Tool is a core abstraction; MCP is an optional protocol/adapter deferred until needed.",
        "Explain portability, reduced lock-in, and a smaller initial agent loop.",
    ),
    "P2C-06": (
        "Preserve Identity -> Policy -> Tool -> Data in order.",
        "Do not describe full family/RBAC authorization as already implemented.",
    ),
    "P2C-07": (
        "The tested Gitleaks 8.30.1 missed a synthetic GitHub PAT; the positive control failed.",
        "Pinned 8.18.4 detected it; do not claim all scanner versions fail.",
    ),
    "P2C-08": (
        "Thinking tokens consumed num_predict=32 before final content could be emitted.",
        "think:false validated deterministic Phase 1 functional output.",
    ),
    "P2C-09": (
        "State ~/.hiwan/dev/databases/hiwan.db (outside the Git repository).",
        "Do not say the actual private DB is committed to Git.",
    ),
    "P2C-10": (
        "Describe the demonstrated path: prompt, agent, identity/policy, local tool, LLM answer, SQLite.",
        "Separate proven tracer-bullet behavior from future production reliability.",
    ),
    "P2C-11": (
        "Explain punctuation/term matching, repetition/authority ranking, and grounding errors.",
        "Mention the incorrect .gitignore-primary-boundary answer if supported.",
    ),
    "P2C-12": (
        "Attribute concern about heavy governance and documentation overhead to Gemini.",
        "Capture proportionate review thresholds for a solo developer; avoid inventing Gemini claims.",
    ),
}

CITATION_RE = re.compile(r"\[S\d+\]")


def source_details(result: Any) -> list[dict[str, Any]]:
    return [
        {
            "label": item.label,
            "path": item.hit.path,
            "heading": item.hit.heading,
            "reference": item.location,
            "start_line": item.hit.start_line,
            "end_line": item.hit.end_line,
            "snippet": item.hit.snippet,
        }
        for item in result.evidence
    ]


def mechanical_checks(answer: str, evidence: list[dict[str, Any]],
                      expected_paths: list[str]) -> dict[str, Any]:
    """Mechanical observability only. Never treat this as correctness."""
    labels_used = sorted(set(CITATION_RE.findall(answer)))
    labels_allowed = {f"[{ev['label']}]" for ev in evidence}
    sources = {ev["path"] for ev in evidence}
    return {
        "answer_nonempty": bool(answer.strip()),
        "selected_evidence_count": len(evidence),
        "expected_source_selected": bool(sources & set(expected_paths)),
        "has_citation_marker": bool(labels_used),
        "used_citation_labels": labels_used,
        "unknown_citation_labels": sorted(set(labels_used) - labels_allowed),
    }


def markdown_review(report: dict[str, Any]) -> str:
    out = [
        "# Phase 2C — Local Qwen Answer Review",
        "",
        f"Run: `{report['run_id']}`",
        f"Model: `{report['model']}`",
        f"Cases attempted: {len(report['cases'])}",
        "",
        "> This is a human-review worksheet, NOT an automatic pass/fail for semantic accuracy.",
        "> Evidence references identify retrieved text, not proof that each generated claim is supported.",
        "",
    ]
    for case in report["cases"]:
        out.extend([
            f"## {case['id']} — {case['category']}",
            "",
            f"**Question:** {case['question']}",
            "",
            f"**Execution:** {case['execution']}",
            "",
        ])
        if case["error"]:
            out.append(f"**Runtime error:** `{case['error']}`")
            out.append("")
        else:
            out.extend(["**Answer:**", "", case["answer"], ""])
        out.append("**Selected evidence:**")
        out.append("")
        if case["evidence"]:
            for ev in case["evidence"]:
                out.append(f"- [{ev['label']}] `{ev['reference']}` — {ev['heading']}")
        else:
            out.append("- None")
        out.extend([
            "",
            "**Mechanical checks (not semantic verdict):**",
            "",
            f"- Expected source selected: `{case['mechanical_checks']['expected_source_selected']}`",
            f"- Citation marker present: `{case['mechanical_checks']['has_citation_marker']}`",
            f"- Invalid citation labels: `{case['mechanical_checks']['unknown_citation_labels']}`",
            "",
            "**Human review checklist:**",
            "",
        ])
        for item in case["review_guide"]:
            out.append(f"- [ ] {item}")
        out.extend([
            "- [ ] Every important factual claim is supported by a cited excerpt.",
            "- [ ] No contradiction of canonical decisions or unsupported overclaim.",
            "- [ ] Answer is complete, readable, and appropriately qualified.",
            "",
            "**Human verdict:** PASS / FAIL / NEEDS MORE EVIDENCE (select one)",
            "",
        ])
    return "\n".join(out) + "\n"


def write_private_reports(report: dict[str, Any], outdir: Path) -> tuple[Path, Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    stem = report["run_id"]
    json_path = outdir / f"{stem}.json"
    md_path = outdir / f"{stem}.md"
    if json_path.exists() or md_path.exists():
        raise FileExistsError(f"report path already exists: {stem}")
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown_review(report), encoding="utf-8")
    json_path.chmod(0o600)
    md_path.chmod(0o600)
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.home() / "hiwan-ai")
    parser.add_argument("--cases", type=Path, default=None)
    parser.add_argument("--outdir", type=Path,
                        default=Path.home() / ".hiwan/dev/logs")
    parser.add_argument("--model", default="qwen3.5:27b-mlx")
    parser.add_argument("--only", nargs="*", default=[], metavar="CASE_ID",
                        help="Run just these case IDs (default: all 12)")
    args = parser.parse_args()
    os.umask(0o077)

    repo = args.repo.expanduser().resolve()
    case_path = args.cases or (repo / "experiments/phase2c_cases.json")
    cases = json.loads(case_path.read_text(encoding="utf-8"))
    all_ids = {str(case["id"]) for case in cases}
    if len(all_ids) != len(cases) or all_ids != set(REVIEW_GUIDE):
        raise ValueError("Evaluation cases differ from the review guide; reconcile before running")
    selected_ids = set(args.only)
    if unknown_ids := selected_ids - all_ids:
        raise ValueError(f"Unknown case IDs: {sorted(unknown_ids)}")
    if selected_ids:
        cases = [case for case in cases if case["id"] in selected_ids]

    from hiwan_ai.knowledge import MarkdownKnowledgeBase
    from hiwan_ai.knowledge_agent import KnowledgeAgent
    from hiwan_ai.llm import OllamaClient

    agent = KnowledgeAgent(
        llm=OllamaClient(model=args.model),
        knowledge_base=MarkdownKnowledgeBase(repo),
        max_hits=3,
    )
    run_id = datetime.now(timezone.utc).strftime("phase2c-answers-%Y%m%dT%H%M%S%fZ")
    report: dict[str, Any] = {
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": str(repo),
        "model": args.model,
        "semantics_verified": False,
        "description": "Local LLM answer collection with manual review guide",
        "cases": [],
    }

    print("========== PHASE 2C REAL ANSWER EVALUATION ==========")
    print("Cases:", len(cases))
    print("Model:", args.model)
    print("Corpus:", repo)
    print("Private report directory:", args.outdir)
    print("No automatic semantic PASS will be claimed.")

    for case in cases:
        start = time.monotonic()
        answer, error, evidence = "", None, []
        try:
            result = agent.answer(str(case["question"]))
            answer = result.answer
            evidence = source_details(result)
            execution = "ANSWERED" if answer.strip() else "EMPTY"
        except Exception as exc:
            execution = "ERROR"
            error = f"{type(exc).__name__}: {exc}"

        checks = mechanical_checks(answer, evidence, list(case["expected_any"]))
        record = {
            "id": case["id"],
            "category": case["category"],
            "question": case["question"],
            "expected_any": case["expected_any"],
            "execution": execution,
            "error": error,
            "elapsed_seconds": round(time.monotonic() - start, 2),
            "answer": answer,
            "evidence": evidence,
            "mechanical_checks": checks,
            "review_guide": REVIEW_GUIDE[case["id"]],
            "human_verdict": None,
        }
        report["cases"].append(record)
        print(f"{case['id']} | {execution} | source-selected={checks['expected_source_selected']} "
              f"| citation={checks['has_citation_marker']} | seconds={record['elapsed_seconds']}")
        if error:
            print("  error:", error)
        elif answer:
            print("  excerpt:", " ".join(answer.split())[:180])

    paths = write_private_reports(report, args.outdir.expanduser())
    print("\n========== SUMMARY ==========")
    print("Answered:", sum(c["execution"] == "ANSWERED" for c in report["cases"]),
          "/", len(report["cases"]))
    print("Expected source present:",
          sum(c["mechanical_checks"]["expected_source_selected"] for c in report["cases"]),
          "/", len(report["cases"]))
    print("Cited at least once:",
          sum(c["mechanical_checks"]["has_citation_marker"] for c in report["cases"]),
          "/", len(report["cases"]))
    print("JSON report:", paths[0])
    print("Human-review worksheet:", paths[1])
    print("Semantic correctness: NOT YET ASSESSED")
    return 0 if all(c["execution"] != "ERROR" for c in report["cases"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())

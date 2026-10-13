"""Minimal, local-only command line entry point for Hiwan knowledge Q&A.

Usage: uv run python -m hiwan_ai ask "What is the privacy boundary?"

The knowledge root is the project checkout containing this package; no private
paths or arbitrary corpora are accepted in this initial CLI.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Sequence


def build_agent(model: str):
    """Build the already-verified retrieval + grounding stack on demand."""
    from .knowledge import MarkdownKnowledgeBase
    from .knowledge_agent import KnowledgeAgent
    from .llm import OllamaClient

    repo = Path(__file__).resolve().parent.parent
    if not (repo / 'DECISIONS.md').is_file():
        raise RuntimeError(
            'Hiwan repository not found beside the installed package. '
            'Run from the ~/hiwan-ai source checkout with `uv run python -m hiwan_ai`.'
        )
    return KnowledgeAgent(
        llm=OllamaClient(model=model),
        knowledge_base=MarkdownKnowledgeBase(repo),
        max_hits=3,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='python -m hiwan_ai',
        description='Hiwan AI — local-first, evidence-grounded project Q&A',
    )
    commands = parser.add_subparsers(dest='command', required=True)
    ask_parser = commands.add_parser('ask', help='Ask about the public project Markdown knowledge')
    ask_parser.add_argument('question', nargs='+', help='Question to answer; quote multiword questions')
    ask_parser.add_argument('--model', default='qwen3.5:27b-mlx',
                            help='Local Ollama model (default: qwen3.5:27b-mlx)')
    args = parser.parse_args(argv)

    if args.command == 'ask':
        question = ' '.join(args.question).strip()
        if not question:
            print('ERROR: Please enter a non-empty question.', file=sys.stderr)
            return 2
        try:
            answer = build_agent(args.model).answer(question)
        except (OSError, RuntimeError, ValueError) as exc:
            print(f'ERROR: {exc}', file=sys.stderr)
            return 1

        print(answer.answer)
        if not answer.evidence:
            print('\nNo relevant supporting evidence was selected.', file=sys.stderr)
            return 3

        print('\nSources (retrieved evidence; citations are not independently fact-checked):')
        for evidence in answer.evidence:
            print(f'  [{evidence.label}] {evidence.location} — {evidence.hit.heading}')
        return 0

    parser.error('Unknown command')
    return 2

from pathlib import Path

from hiwan_ai.knowledge import MarkdownKnowledgeBase
from hiwan_ai.evidence import select_evidence


def main() -> int:
    kb = MarkdownKnowledgeBase(Path.home() / 'hiwan-ai')
    docs = kb.discover()
    q = 'Public Software Private Data'
    candidates = kb.search(q, limit=20)
    chosen = select_evidence(q, candidates, limit=3)
    print('Markdown documents:', len(docs))
    print('Question:', q)
    print('Relevant passages:', len(candidates))
    print('Top candidate:', candidates[0].reference if candidates else None)
    print('Selected evidence:')
    for e in chosen:
        print(f'  [{e.label}] {e.location} | {e.hit.heading} | relevance={e.hit.score}')
    if not docs or not chosen:
        print('FAIL: discovery or evidence selection returned nothing')
        return 1
    if not any(e.hit.path == 'DECISIONS.md' for e in chosen):
        print('FAIL: formal decision missing from evidence on this policy question')
        return 1
    print('PASS: relevant retrieval and authority-aware evidence selection')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

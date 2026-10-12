from pathlib import Path

from hiwan_ai.knowledge import MarkdownKnowledgeBase
from hiwan_ai.knowledge_agent import KnowledgeAgent
from hiwan_ai.llm import OllamaClient


def main() -> int:
    kb = MarkdownKnowledgeBase(Path.home() / 'hiwan-ai')
    agent = KnowledgeAgent(
        llm=OllamaClient(model='qwen3.5:27b-mlx'),
        knowledge_base=kb,
        max_hits=3,
    )
    question = 'What is the Public Software Private Data boundary in Hiwan AI?'
    result = agent.answer(question)
    print('Question:', question)
    print('Answer:', result.answer)
    print('Evidence supplied to model:')
    for item in result.evidence:
        print(f'  [{item.label}] {item.location}: {item.hit.heading}')
    if not result.answer or not result.evidence:
        print('FAIL: no answer or evidence')
        return 1
    if result.evidence[0].hit.path != 'DECISIONS.md':
        print('FAIL: accepted decision was not selected first for this policy question')
        return 1
    print('PASS: answer generated with inspectable policy evidence')
    print('NOTE: human review is still required for semantic correctness')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

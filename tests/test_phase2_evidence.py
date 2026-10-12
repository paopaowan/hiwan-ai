from pathlib import Path

from hiwan_ai.evidence import select_evidence
from hiwan_ai.knowledge import MarkdownKnowledgeBase
from hiwan_ai.knowledge_agent import KnowledgeAgent
from hiwan_ai.llm import LLMResponse


def corpus(root: Path) -> MarkdownKnowledgeBase:
    (root / 'DECISIONS.md').write_text(
        '# Architecture Decisions\n\n'
        '## Decision 010 — Public Software / Private Data Boundary\n\n'
        'Accepted: public software repository remains separate from private data.\n'
        'Private runtime data lives outside the Git tree at ~/.hiwan.\n\n'
        '## Decision 011 — Physical Private Data Boundary\n\n'
        'Physical separation is the primary control; .gitignore is defense-in-depth.\n',
        encoding='utf-8',
    )
    (root / 'ARCHITECTURE.md').write_text(
        '# Architecture\n\n'
        '## Public Software / Private Data Boundary\n\n'
        'A diagram of the architecture: public repository and private data.\n',
        encoding='utf-8',
    )
    reviews = root / 'architecture' / 'reviews' / 'gemini'
    reviews.mkdir(parents=True)
    (reviews / 'gemini-review.md').write_text(
        '# Gemini Review\n\n'
        '## Review of Public Software Private Data Boundary\n\n'
        + ('Public Software Private Data Boundary, ' * 100)
        + '\nGemini suggests physical separation.\n',
        encoding='utf-8',
    )
    return MarkdownKnowledgeBase(root)


def test_repetition_does_not_force_review_to_win(tmp_path):
    kb = corpus(tmp_path)
    question = 'What is the Public Software Private Data boundary in Hiwan AI?'
    candidates = kb.search(question, limit=20)
    evidence = select_evidence(question, candidates, limit=3)
    assert evidence
    assert evidence[0].hit.path == 'DECISIONS.md'
    assert evidence[0].hit.start_line > 1
    assert any(e.hit.path == 'DECISIONS.md' for e in evidence)


def test_gemini_review_question_uses_review_as_primary_evidence(tmp_path):
    kb = corpus(tmp_path)
    q = 'What did Gemini review say about the Public Software Private Data boundary?'
    candidates = kb.search(q, limit=20)
    evidence = select_evidence(q, candidates, limit=3)
    assert evidence
    assert 'gemini' in evidence[0].hit.path


def test_unrelated_decision_cannot_win_by_authority(tmp_path):
    (tmp_path / 'DECISIONS.md').write_text('# Decisions\n\nUnrelated budget limits\n')
    (tmp_path / 'README.md').write_text('# Project\n\nSourdough fermentation requires yeast.\n')
    kb = MarkdownKnowledgeBase(tmp_path)
    evidence = select_evidence('sourdough fermentation',
                               kb.search('sourdough fermentation'))
    assert evidence[0].hit.path == 'README.md'


def test_discovery_skips_private_paths_and_symlinks(tmp_path):
    kb = corpus(tmp_path)
    secret_dir = tmp_path / 'private'
    secret_dir.mkdir()
    (secret_dir / 'secrets.md').write_text('private family secret', encoding='utf-8')
    outside = tmp_path.parent / (tmp_path.name + '_outside.md')
    outside.write_text('outside repository private data', encoding='utf-8')
    (tmp_path / 'linked.md').symlink_to(outside)
    try:
        paths = [d.path for d in kb.discover()]
        assert 'private/secrets.md' not in paths
        assert 'linked.md' not in paths
    finally:
        outside.unlink(missing_ok=True)


class FakeLLM:
    def __init__(self):
        self.messages = []

    def chat(self, messages, **kwargs):
        self.messages.append(messages)
        return LLMResponse(
            content='Primary boundary is physical separation [S1].',
            thinking='', done_reason='stop', prompt_eval_count=1,
            prompt_eval_duration_ns=1, eval_count=1, eval_duration_ns=1,
        )


def test_answer_provenance_maps_to_real_section(tmp_path):
    kb = corpus(tmp_path)
    fake = FakeLLM()
    result = KnowledgeAgent(llm=fake, knowledge_base=kb).answer(
        'What is the Public Software Private Data boundary in Hiwan AI?'
    )
    assert result.sources[0] == 'DECISIONS.md'
    assert result.evidence[0].location.startswith('DECISIONS.md:L')
    assert '[S1]' in fake.messages[0][0]['content']


def test_no_evidence_skips_llm(tmp_path):
    kb = corpus(tmp_path)
    fake = FakeLLM()
    result = KnowledgeAgent(llm=fake, knowledge_base=kb).answer(
        'quantum chromodynamics'
    )
    assert not result.evidence
    assert not fake.messages


def test_invalid_model_citation_is_rejected(tmp_path):
    kb = corpus(tmp_path)

    class BadCitationLLM(FakeLLM):
        def chat(self, messages, **kwargs):
            result = super().chat(messages, **kwargs)
            return LLMResponse(
                content='This claim [S99] is unsupported.',
                thinking='', done_reason='stop', prompt_eval_count=1,
                prompt_eval_duration_ns=1, eval_count=1, eval_duration_ns=1,
            )

    agent = KnowledgeAgent(llm=BadCitationLLM(), knowledge_base=kb)
    try:
        agent.answer('What is the Public Software Private Data boundary?')
    except ValueError as exc:
        assert 'unknown evidence labels' in str(exc)
    else:
        raise AssertionError('expected unknown citation label rejection')

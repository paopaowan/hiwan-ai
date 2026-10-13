"""CLI smoke tests use stubs and never call the local model or private data."""
from types import SimpleNamespace

import pytest

from hiwan_ai import cli


def _result(answer='Supported statement [S1]', *, evidence=True):
    sources = ()
    if evidence:
        hit = SimpleNamespace(heading='Decision 011 — Physical Private Data Boundary')
        sources = (SimpleNamespace(
            label='S1',
            location='DECISIONS.md:L174-L210',
            hit=hit,
        ),)
    return SimpleNamespace(answer=answer, evidence=sources)


def test_help_never_constructs_ollama(monkeypatch, capsys):
    monkeypatch.setattr(cli, 'build_agent', lambda model: pytest.fail('model loaded during help'))
    with pytest.raises(SystemExit) as exc:
        cli.main(['--help'])
    assert exc.value.code == 0
    assert 'ask' in capsys.readouterr().out


def test_ask_prints_answer_and_exact_evidence_locations(monkeypatch, capsys):
    seen = {}

    class FakeAgent:
        def answer(self, question):
            seen['question'] = question
            return _result()

    def fake_build(model):
        seen['model'] = model
        return FakeAgent()

    monkeypatch.setattr(cli, 'build_agent', fake_build)
    assert cli.main(['ask', 'Where is private data?', '--model', 'test-local']) == 0
    output = capsys.readouterr().out
    assert seen == {'model': 'test-local', 'question': 'Where is private data?'}
    assert 'Supported statement [S1]' in output
    assert '[S1] DECISIONS.md:L174-L210' in output
    assert 'Sources' in output


def test_no_relevant_evidence_is_not_success(monkeypatch, capsys):
    monkeypatch.setattr(cli, 'build_agent', lambda model: SimpleNamespace(
        answer=lambda question: _result('Insufficient evidence', evidence=False)
    ))
    assert cli.main(['ask', 'unknown subject']) == 3
    output = capsys.readouterr()
    assert 'Insufficient evidence' in output.out
    assert 'No relevant supporting evidence' in output.err


def test_blank_question_fails_before_model_loading(monkeypatch, capsys):
    monkeypatch.setattr(cli, 'build_agent', lambda model: pytest.fail('model loaded with blank input'))
    assert cli.main(['ask', '    ']) == 2
    assert 'non-empty question' in capsys.readouterr().err


def test_local_ollama_error_produces_nonzero_exit(monkeypatch, capsys):
    def fail(model):
        raise RuntimeError('Ollama unreachable')
    monkeypatch.setattr(cli, 'build_agent', fail)
    assert cli.main(['ask', 'test question']) == 1
    assert 'Ollama unreachable' in capsys.readouterr().err

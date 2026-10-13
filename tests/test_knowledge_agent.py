from pathlib import Path

from hiwan_ai.knowledge import MarkdownKnowledgeBase
from hiwan_ai.knowledge_agent import KnowledgeAgent
from hiwan_ai.llm import LLMResponse


def response(content: str) -> LLMResponse:
    return LLMResponse(
        content=content,
        thinking="",
        done_reason="stop",
        prompt_eval_count=1,
        prompt_eval_duration_ns=1,
        eval_count=1,
        eval_duration_ns=1,
    )


class FakeLLM:
    def __init__(self, output: str) -> None:
        self.output = output
        self.calls = []

    def chat(self, messages, **kwargs) -> LLMResponse:
        self.calls.append((messages, kwargs))
        return response(self.output)


def test_knowledge_agent_retrieves_context_and_returns_sources(tmp_path: Path) -> None:
    (tmp_path / "DECISIONS.md").write_text(
        "# Architecture Decisions\n\n"
        "## Public Software / Private Data Boundary\n\n"
        "The public repository is ~/hiwan-ai.\n\n"
        "Private runtime data is physically outside Git at ~/.hiwan.\n",
        encoding="utf-8",
    )

    llm = FakeLLM(
        "The public repository is ~/hiwan-ai and private runtime data "
        "is physically separated under ~/.hiwan [S1]."
    )
    agent = KnowledgeAgent(
        llm=llm,
        knowledge_base=MarkdownKnowledgeBase(tmp_path),
        max_hits=3,
    )

    result = agent.answer(
        "What is the Public Software Private Data boundary in Hiwan AI?"
    )

    assert result.sources[0] == "DECISIONS.md"
    assert result.hits[0].path == "DECISIONS.md"

    messages, kwargs = llm.calls[0]
    prompt = "\n".join(message["content"] for message in messages)
    assert [m["role"] for m in messages] == ["system", "user"]

    assert "DECISIONS.md" in prompt
    assert "~/.hiwan" in prompt
    assert "supplied evidence" in prompt
    assert kwargs["think"] is False
    assert kwargs["temperature"] == 0.0


def test_knowledge_agent_returns_no_sources_when_retrieval_is_empty(
    tmp_path: Path,
) -> None:
    (tmp_path / "README.md").write_text(
        "# Project\n\nNothing about astronomy here.\n",
        encoding="utf-8",
    )

    llm = FakeLLM("should not be used")
    agent = KnowledgeAgent(
        llm=llm,
        knowledge_base=MarkdownKnowledgeBase(tmp_path),
    )

    result = agent.answer("quantum chromodynamics")

    assert result.sources == ()
    assert result.hits == ()
    assert "could not find" in result.answer.casefold()
    assert llm.calls == []


def test_knowledge_agent_rejects_empty_question(tmp_path: Path) -> None:
    llm = FakeLLM("unused")
    agent = KnowledgeAgent(
        llm=llm,
        knowledge_base=MarkdownKnowledgeBase(tmp_path),
    )

    try:
        agent.answer("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    assert llm.calls == []

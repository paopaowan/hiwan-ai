from hiwan_ai.llm import LLMResponse

def test_generation_rate():
    r = LLMResponse(
        content="ok",
        thinking="",
        done_reason="stop",
        prompt_eval_count=0,
        prompt_eval_duration_ns=0,
        eval_count=16,
        eval_duration_ns=1_000_000_000,
    )
    assert r.generation_tokens_per_second == 16.0

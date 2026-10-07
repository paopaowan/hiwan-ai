from hiwan_ai import OllamaClient

EXPECTED = "HIWAN_LOCAL_AI_OK"

def main():
    client = OllamaClient()
    r = client.chat(
        [{"role": "user", "content": f"Reply with exactly: {EXPECTED}"}],
        think=False,
        num_ctx=8192,
        num_predict=32,
    )
    print("Response:", repr(r.content.strip()))
    print("Thinking chars:", len(r.thinking))
    print("Done reason:", r.done_reason)
    print("Generated tokens:", r.eval_count)
    print("Generation tok/s:", round(r.generation_tokens_per_second, 2) if r.generation_tokens_per_second else "N/A")
    if r.content.strip() != EXPECTED or r.thinking:
        print("FAIL: minimal LLM client smoke test failed")
        return 1
    print("PASS: minimal LLM client works")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

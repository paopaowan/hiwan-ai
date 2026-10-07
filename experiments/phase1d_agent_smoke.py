from hiwan_ai.agent import AgentContext, MinimalAgent
from hiwan_ai.llm import OllamaClient


EXPECTED = "HIWAN_AGENT_OK"


def main() -> int:
    llm = OllamaClient(model="qwen3.5:27b-mlx")
    agent = MinimalAgent(llm)

    result = agent.run(
        f"Reply with exactly: {EXPECTED}",
        context=AgentContext(identity="richard"),
    )

    print("Identity:", result.identity)
    print("Response:", repr(result.content.strip()))
    print("Done reason:", result.done_reason)

    if result.identity != "richard":
        print("FAIL: identity was not preserved")
        return 1

    if result.content.strip() != EXPECTED:
        print("FAIL: response did not match expected output")
        return 1

    print("PASS: minimal agent loop works")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from hiwan_ai.agent import AgentContext, MinimalAgent
from hiwan_ai.llm import OllamaClient
from hiwan_ai.tools import LocalSystemInfoTool


def main() -> int:
    agent = MinimalAgent(
        OllamaClient(model="qwen3.5:27b-mlx"),
        tools=[LocalSystemInfoTool()],
    )

    result = agent.run(
        "What CPU architecture is the machine running Hiwan AI on? "
        "Use the local_system_info tool.",
        context=AgentContext(identity="richard"),
    )

    print("Identity:", result.identity)
    print("Tool used:", result.tool_used)
    print("Tool result:", result.tool_result)
    print("Response:", repr(result.content.strip()))

    if result.tool_used != "local_system_info":
        print("FAIL: expected local_system_info tool")
        return 1

    if "architecture=" not in (result.tool_result or ""):
        print("FAIL: tool did not return architecture")
        return 1

    print("PASS: agent selected and executed one local tool")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

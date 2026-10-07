from hiwan_ai.tools import LocalSystemInfoTool


def test_local_system_info_tool_returns_architecture() -> None:
    result = LocalSystemInfoTool().run({})
    assert "os=" in result
    assert "architecture=" in result


def test_local_system_info_rejects_arguments() -> None:
    tool = LocalSystemInfoTool()

    try:
        tool.run({"unexpected": True})
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

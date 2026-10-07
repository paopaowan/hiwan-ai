from __future__ import annotations

from dataclasses import dataclass
import platform
from typing import Any, Protocol


class Tool(Protocol):
    name: str
    description: str

    def run(self, arguments: dict[str, Any]) -> str: ...


@dataclass(frozen=True)
class LocalSystemInfoTool:
    """Safe, read-only Phase 1 local tool."""

    name: str = "local_system_info"
    description: str = (
        "Return local machine OS and CPU architecture. "
        "Use this when the user asks about the machine running Hiwan AI."
    )

    def run(self, arguments: dict[str, Any]) -> str:
        if arguments:
            raise ValueError("local_system_info does not accept arguments")

        return (
            f"os={platform.system()} "
            f"release={platform.release()} "
            f"architecture={platform.machine()}"
        )

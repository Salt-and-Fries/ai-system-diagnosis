from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ToolResult:
    success: bool
    data: Any
    error: str | None = None


class BaseTool:
    name: str
    description: str
    parameters_schema: Dict[str, Any]

    def run(self, **kwargs) -> ToolResult:  # pragma: no cover - interface
        raise NotImplementedError

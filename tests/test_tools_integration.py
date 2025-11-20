import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if ROOT.as_posix() not in sys.path:
    sys.path.insert(0, ROOT.as_posix())

from src.config import Config
from src.agent.tools_registry import get_tools_registry
from src.tools.base import ToolResult


def test_tools_run_without_exceptions():
    config = Config(openai_api_key=None, model_name="test", mode="diagnostic_only", confirm_fixes=True)
    registry = get_tools_registry(config)

    for name, tool in registry.items():
        if name in {"restart_service", "run_system_file_check", "disable_startup_item"}:
            # Fix tools should be disabled in diagnostic mode
            result = tool.run(**({"service_name": "Dummy"} if name == "restart_service" else {"name": "Dummy"} if name == "disable_startup_item" else {}))
            assert isinstance(result, ToolResult)
            assert not result.success
            continue

        result = tool.run()
        assert isinstance(result, ToolResult)

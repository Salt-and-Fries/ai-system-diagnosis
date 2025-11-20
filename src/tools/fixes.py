from __future__ import annotations

from ..config import Config
from ..utils.os_detect import is_windows
from ..utils.shell_utils import run_command
from .base import BaseTool, ToolResult


DISABLED_MESSAGE = "Fix operations disabled in this mode."


class RestartServiceTool(BaseTool):
    name = "restart_service"
    description = "Restart a Windows service by name."
    parameters_schema = {
        "type": "object",
        "properties": {
            "service_name": {"type": "string", "description": "Name of the service to restart"}
        },
        "required": ["service_name"],
    }

    def __init__(self, config: Config):
        self.config = config

    def run(self, service_name: str) -> ToolResult:
        if not self.config.allow_fixes:
            return ToolResult(success=False, data={}, error=DISABLED_MESSAGE)
        if not is_windows():
            return ToolResult(success=False, data={}, error="Service control is only supported on Windows")

        success, stdout, stderr = run_command(
            ["powershell", "-Command", f"Restart-Service -Name '{service_name}' -Force"]
        )
        if not success:
            return ToolResult(success=False, data={}, error=stderr or stdout)
        return ToolResult(success=True, data={"message": f"Service {service_name} restarted."})


class SystemFileCheckTool(BaseTool):
    name = "run_system_file_check"
    description = "Run Windows System File Checker (sfc /scannow)."
    parameters_schema: dict = {"type": "object", "properties": {}, "required": []}

    def __init__(self, config: Config):
        self.config = config

    def run(self) -> ToolResult:
        if not self.config.allow_fixes:
            return ToolResult(success=False, data={}, error=DISABLED_MESSAGE)
        if not is_windows():
            return ToolResult(success=False, data={}, error="System file check is only supported on Windows")

        success, stdout, stderr = run_command(["sfc", "/scannow"], timeout=600)
        if not success:
            return ToolResult(success=False, data={}, error=stderr or stdout)

        truncated_output = stdout[-2000:] if stdout else ""
        return ToolResult(success=True, data={"output": truncated_output})


class DisableStartupItemTool(BaseTool):
    name = "disable_startup_item"
    description = "Disable a startup item by name or identifier (not yet implemented)."
    parameters_schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Display name of the startup entry to disable",
            }
        },
        "required": ["name"],
    }

    def __init__(self, config: Config):
        self.config = config

    def run(self, name: str) -> ToolResult:
        if not self.config.allow_fixes:
            return ToolResult(success=False, data={}, error=DISABLED_MESSAGE)
        return ToolResult(success=False, data={}, error="Disabling startup items is not implemented yet")

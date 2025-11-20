from __future__ import annotations

import json

from .base import BaseTool, ToolResult
from ..utils.os_detect import is_windows
from ..utils.shell_utils import run_command


class EventLogsTool(BaseTool):
    name = "get_recent_system_errors"
    description = "Fetch recent error-level events from system logs."
    parameters_schema = {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Maximum number of events to return",
                "default": 50,
            }
        },
        "required": [],
    }

    def run(self, limit: int = 50) -> ToolResult:
        if not is_windows():
            return ToolResult(success=False, data=[], error="Event log inspection is only supported on Windows")

        ps_command = (
            "Get-WinEvent -LogName System -MaxEvents 200 | "
            f"Where-Object {{$_.LevelDisplayName -eq 'Error'}} | Select-Object -First {limit} | "
            "Select-Object TimeCreated, ProviderName, Id, LevelDisplayName, Message | ConvertTo-Json"
        )
        success, stdout, stderr = run_command(["powershell", "-Command", ps_command])
        if not success:
            return ToolResult(success=False, data=[], error=stderr or "Unable to read event logs")

        try:
            events = json.loads(stdout)
        except json.JSONDecodeError:
            events = []

        return ToolResult(success=True, data=events)

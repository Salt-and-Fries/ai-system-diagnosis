from __future__ import annotations

import psutil

from .base import BaseTool, ToolResult


class TemperatureTool(BaseTool):
    name = "get_temperature_readings"
    description = "Attempt to read CPU/GPU temperature sensors."
    parameters_schema: dict = {"type": "object", "properties": {}, "required": []}

    def run(self) -> ToolResult:
        try:
            temps = psutil.sensors_temperatures()
        except (AttributeError, NotImplementedError):
            return ToolResult(success=False, data={}, error="Temperature readings not supported")

        if not temps:
            return ToolResult(success=False, data={}, error="No temperature sensors detected")

        simplified = {label: [entry._asdict() for entry in entries] for label, entries in temps.items()}
        return ToolResult(success=True, data=simplified)

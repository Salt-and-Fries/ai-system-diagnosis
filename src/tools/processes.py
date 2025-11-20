from __future__ import annotations

import psutil

from .base import BaseTool, ToolResult


class ProcessSnapshotTool(BaseTool):
    name = "get_process_snapshot"
    description = "List top processes by CPU usage."
    parameters_schema = {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Max number of processes to return.",
                "default": 20,
            }
        },
        "required": [],
    }

    def run(self, limit: int = 20) -> ToolResult:
        processes = []
        for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
            try:
                info = proc.info
                processes.append(
                    {
                        "pid": info.get("pid"),
                        "name": info.get("name"),
                        "cpu_percent": info.get("cpu_percent"),
                        "memory_mb": round((info.get("memory_info").rss or 0) / (1024 ** 2), 2),
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes_sorted = sorted(processes, key=lambda p: p.get("cpu_percent", 0), reverse=True)
        return ToolResult(success=True, data=processes_sorted[:limit])

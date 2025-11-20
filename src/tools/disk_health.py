from __future__ import annotations

import psutil

from .base import BaseTool, ToolResult
from ..utils.os_detect import is_windows
from ..utils.shell_utils import run_command


class DiskHealthTool(BaseTool):
    name = "get_disk_health"
    description = "Fetch SMART/health status for attached disks."
    parameters_schema: dict = {"type": "object", "properties": {}, "required": []}

    def run(self) -> ToolResult:
        if is_windows():
            success, stdout, stderr = run_command(
                ["wmic", "diskdrive", "get", "Status,Model,Size", "/format:csv"]
            )
            if not success:
                return ToolResult(success=False, data={}, error=stderr or "Unable to query disk health")

            drives = []
            for line in stdout.splitlines():
                if not line or line.lower().startswith("node,"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 4:
                    continue
                _, model, size, status = parts
                try:
                    size_gb = round(int(size) / (1024 ** 3), 2)
                except ValueError:
                    size_gb = 0
                drives.append({"model": model, "size_gb": size_gb, "status": status or "Unknown"})

            return ToolResult(success=True, data={"drives": drives})

        # Fallback for non-Windows systems: provide high-level disk info
        drives = []
        seen_devices = set()
        for part in psutil.disk_partitions(all=False):
            if part.device in seen_devices:
                continue
            seen_devices.add(part.device)
            try:
                usage = psutil.disk_usage(part.mountpoint)
                size_gb = round(usage.total / (1024 ** 3), 2)
            except PermissionError:
                size_gb = 0
            drives.append({"model": part.device, "size_gb": size_gb, "status": "Unknown"})

        return ToolResult(success=True, data={"drives": drives}, error="SMART status not available on this platform")

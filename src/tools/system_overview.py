from __future__ import annotations

import platform
import time
from typing import List

import psutil

from .base import BaseTool, ToolResult
from ..utils.shell_utils import run_command


def _bytes_to_gb(value: float) -> float:
    return round(value / (1024 ** 3), 2)


def _get_gpu_info() -> List[dict]:
    success, stdout, _ = run_command([
        "nvidia-smi",
        "--query-gpu=name,driver_version",
        "--format=csv,noheader",
    ])
    if not success or not stdout:
        return [{"name": "unknown", "driver_version": "unknown"}]

    gpus = []
    for line in stdout.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2:
            gpus.append({"name": parts[0], "driver_version": parts[1]})
    return gpus or [{"name": "unknown", "driver_version": "unknown"}]


class SystemOverviewTool(BaseTool):
    name = "get_system_overview"
    description = "Get summary of OS, CPU, RAM, GPU, and disk usage."
    parameters_schema: dict = {"type": "object", "properties": {}, "required": []}

    def run(self) -> ToolResult:
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)
        virtual_mem = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=0.1)

        disks = []
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
            except PermissionError:
                continue
            disks.append(
                {
                    "device": part.device,
                    "total_gb": _bytes_to_gb(usage.total),
                    "used_gb": _bytes_to_gb(usage.used),
                    "usage_percent": round(usage.percent, 2),
                }
            )

        result = {
            "os": platform.system(),
            "os_version": platform.version(),
            "hostname": platform.node(),
            "uptime_seconds": uptime_seconds,
            "cpu": {
                "model": platform.processor() or "unknown",
                "cores_physical": psutil.cpu_count(logical=False) or 0,
                "cores_logical": psutil.cpu_count(logical=True) or 0,
                "usage_percent": cpu_percent,
            },
            "ram": {
                "total_gb": _bytes_to_gb(virtual_mem.total),
                "used_gb": _bytes_to_gb(virtual_mem.used),
                "usage_percent": round(virtual_mem.percent, 2),
            },
            "gpus": _get_gpu_info(),
            "disks": disks,
        }

        return ToolResult(success=True, data=result)

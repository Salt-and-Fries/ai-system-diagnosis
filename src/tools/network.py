from __future__ import annotations

import platform
import re
import socket
from typing import Any, Dict

from .base import BaseTool, ToolResult
from ..utils.shell_utils import run_command


class NetworkDiagnosticsTool(BaseTool):
    name = "run_network_diagnostics"
    description = "Run ping and DNS checks against a target."
    parameters_schema = {
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target host or IP to test",
                "default": "8.8.8.8",
            }
        },
        "required": [],
    }

    def _ping_target(self, target: str) -> Dict[str, Any]:
        count_flag = "-n" if platform.system().lower() == "windows" else "-c"
        success, stdout, stderr = run_command(["ping", count_flag, "4", target], timeout=15)
        if not success:
            return {"success": False, "error": stderr or stdout}

        # Parse average latency
        avg_match = re.search(r"= [^/]*/([^/]+)/", stdout) or re.search(r"Average = ([0-9.]+)ms", stdout)
        avg_ms = float(avg_match.group(1)) if avg_match else None
        loss_match = re.search(r"(\d+)% packet loss", stdout) or re.search(r"Lost = \d+ \((\d+)% loss\)", stdout)
        packet_loss = float(loss_match.group(1)) if loss_match else 0

        return {"success": True, "avg_ms": avg_ms, "packet_loss_percent": packet_loss}

    def _dns_lookup(self, target: str) -> Dict[str, Any]:
        try:
            ip = socket.gethostbyname(target)
            return {"success": True, "resolved_ip": ip}
        except socket.gaierror as exc:
            return {"success": False, "error": str(exc)}

    def run(self, target: str = "8.8.8.8") -> ToolResult:
        ping_result = self._ping_target(target)
        dns_result = self._dns_lookup(target)

        return ToolResult(
            success=True,
            data={"target": target, "ping": ping_result, "dns": dns_result},
        )

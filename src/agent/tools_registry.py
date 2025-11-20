from __future__ import annotations

from typing import Dict

from ..config import Config
from ..tools import (
    DiskHealthTool,
    DisableStartupItemTool,
    EventLogsTool,
    NetworkDiagnosticsTool,
    ProcessSnapshotTool,
    RestartServiceTool,
    SystemFileCheckTool,
    SystemOverviewTool,
    TemperatureTool,
)
from ..tools.base import BaseTool


FIX_TOOL_NAMES = {"restart_service", "run_system_file_check", "disable_startup_item"}


def get_tools_registry(config: Config) -> Dict[str, BaseTool]:
    return {
        "get_system_overview": SystemOverviewTool(),
        "get_process_snapshot": ProcessSnapshotTool(),
        "get_disk_health": DiskHealthTool(),
        "get_recent_system_errors": EventLogsTool(),
        "run_network_diagnostics": NetworkDiagnosticsTool(),
        "get_temperature_readings": TemperatureTool(),
        "restart_service": RestartServiceTool(config),
        "run_system_file_check": SystemFileCheckTool(config),
        "disable_startup_item": DisableStartupItemTool(config),
    }

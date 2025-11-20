import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if ROOT.as_posix() not in sys.path:
    sys.path.insert(0, ROOT.as_posix())

from src.tools.system_overview import SystemOverviewTool


def test_system_overview_keys_present():
    tool = SystemOverviewTool()
    result = tool.run()
    assert result.success
    data = result.data
    for key in ["os", "os_version", "hostname", "uptime_seconds", "cpu", "ram", "gpus", "disks"]:
        assert key in data
    assert "model" in data["cpu"]
    assert "total_gb" in data["ram"]

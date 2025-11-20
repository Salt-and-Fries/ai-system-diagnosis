import subprocess
from typing import List, Tuple


def run_command(command: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
    """Run a command and return (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return (result.returncode == 0, result.stdout.strip(), result.stderr.strip())
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, "", str(exc)

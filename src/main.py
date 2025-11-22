from __future__ import annotations

import argparse
import importlib.util
import sys
from typing import Tuple

from .agent.conversation import ConversationRunner
from .config import load_config
from .utils.logging_utils import setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI system diagnoser")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--diagnostic-only", action="store_true", help="Disable fix operations")
    group.add_argument("--allow-fixes", action="store_true", help="Enable fix operations")
    parser.add_argument("--cli", action="store_true", help="Use the terminal interface instead of the UI")
    return parser.parse_args()


def _can_launch_ui() -> Tuple[bool, str | None]:
    """Check whether the Tk UI can start in this environment."""

    try:
        import tkinter as tk  # noqa: F401
    except Exception as exc:  # pragma: no cover - environment dependent
        return False, f"Tkinter is unavailable ({exc})"

    if not importlib.util.find_spec("tkhtmlview"):
        return False, "UI dependencies are missing. Install with 'pip install .[ui]' or rerun with --cli."

    try:
        import tkinter as tk  # type: ignore  # noqa: F811

        root = tk.Tk()
        root.withdraw()
        root.update_idletasks()
    except Exception as exc:  # pragma: no cover - environment dependent
        return False, f"Unable to initialize Tk display ({exc})"
    finally:
        try:
            root.destroy()
        except Exception:
            pass

    return True, None


def main():
    args = parse_args()
    config = load_config()

    if args.allow_fixes:
        config.mode = "allow_fixes"
    elif args.diagnostic_only:
        config.mode = "diagnostic_only"

    if not config.openai_api_key:
        print("OPENAI_API_KEY is not set. Please configure it in your environment or .env file.")
        return

    logger = setup_logging()
    logger.info("Starting ai-system-diagnoser in %s mode", config.mode)
    logger.info("Using AI model: %s", config.model_name)

    runner = ConversationRunner(config)
    if args.cli:
        runner.run_conversation()
        return

    can_launch, reason = _can_launch_ui()
    if not can_launch:
        print(f"UI unavailable: {reason}\nFalling back to CLI...")
        runner.run_conversation()
        return

    from .ui import ChatWindow

    app = ChatWindow(runner)
    app.run()


if __name__ == "__main__":  # pragma: no cover
    main()

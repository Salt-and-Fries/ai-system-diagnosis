from __future__ import annotations

import argparse
import importlib.util
import sys

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

    if sys.version_info >= (3, 14):
        print(
            "UI dependencies are not available on Python 3.14 yet. "
            "Run with --cli or install on Python 3.10-3.13 to use the UI."
        )
        runner.run_conversation()
        return

    if not importlib.util.find_spec("tkhtmlview"):
        print(
            "UI dependencies are missing. Install with 'pip install .[ui]' or rerun with --cli."
        )
        runner.run_conversation()
        return

    from .ui import ChatWindow

    app = ChatWindow(runner)
    app.run()


if __name__ == "__main__":  # pragma: no cover
    main()

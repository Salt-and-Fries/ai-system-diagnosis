from __future__ import annotations

import argparse

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
    else:
        from .ui import ChatWindow

        app = ChatWindow(runner)
        app.run()


if __name__ == "__main__":  # pragma: no cover
    main()

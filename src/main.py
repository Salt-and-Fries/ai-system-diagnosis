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
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config()

    if args.allow_fixes:
        config.mode = "allow_fixes"
    elif args.diagnostic_only:
        config.mode = "diagnostic_only"

    logger = setup_logging()
    logger.info("Starting ai-system-diagnoser in %s mode", config.mode)
    logger.info("Using AI model: %s", config.model_name)

    runner = ConversationRunner(config)
    runner.run_conversation()


if __name__ == "__main__":  # pragma: no cover
    main()

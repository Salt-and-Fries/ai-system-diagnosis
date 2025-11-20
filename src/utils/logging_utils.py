import logging
from pathlib import Path
from typing import Optional

DEFAULT_LOG_PATH = Path("ai-system-diagnoser.log")


def setup_logging(log_path: Optional[Path] = None) -> logging.Logger:
    log_file = log_path or DEFAULT_LOG_PATH
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ai_system_diagnoser")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

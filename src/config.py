from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration derived from environment variables."""

    openai_api_key: Optional[str]
    model_name: str
    mode: str
    confirm_fixes: bool

    @property
    def allow_fixes(self) -> bool:
        return self.mode.lower() == "allow_fixes"


DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_MODE = "diagnostic_only"
DEFAULT_CONFIRM_FIXES = True


def load_config(env_path: Path | None = None) -> Config:
    """Load configuration from environment variables, optionally from a .env file."""

    env_file = env_path or Path.cwd() / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    openai_api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME", DEFAULT_MODEL)
    mode = os.getenv("MODE", DEFAULT_MODE)
    confirm_fixes_env = os.getenv("CONFIRM_FIXES")
    confirm_fixes = (
        DEFAULT_CONFIRM_FIXES
        if confirm_fixes_env is None
        else confirm_fixes_env.lower() in {"1", "true", "yes"}
    )

    return Config(
        openai_api_key=openai_api_key,
        model_name=model_name,
        mode=mode,
        confirm_fixes=confirm_fixes,
    )

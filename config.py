import os
from pathlib import Path


# Project information
PROJECT_NAME = "EmpirE Downloader"
VERSION = "0.1.0"

# Telegram bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Language settings
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "fa"]

# Download settings
DOWNLOAD_DIR = Path("downloads")
MAX_FILE_SIZE_MB = 50

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def validate_config():
    """Check required configuration."""
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing. Set it as an environment variable."
        )
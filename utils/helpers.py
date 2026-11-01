import re
from pathlib import Path
from urllib.parse import urlparse


SUPPORTED_SCHEMES = ("http", "https")


def is_valid_url(url: str) -> bool:
    """Check whether a URL has a valid HTTP or HTTPS structure."""

    if not isinstance(url, str):
        return False

    url = url.strip()

    if not url or any(char.isspace() for char in url):
        return False

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme.lower() in SUPPORTED_SCHEMES
            and bool(parsed.netloc)
            and bool(parsed.hostname)
            and "." in parsed.hostname
        )
    except (ValueError, AttributeError):
        return False


def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters from a filename."""

    filename = Path(filename).name
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", filename)
    filename = filename.strip(" .")

    if not filename:
        return "download"

    return filename[:200]


def format_file_size(size_bytes: int) -> str:
    """Convert a file size in bytes into a readable format."""

    if size_bytes < 0:
        return "Unknown size"

    units = ("B", "KB", "MB", "GB", "TB")
    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"

        size /= 1024

    return "Unknown size"
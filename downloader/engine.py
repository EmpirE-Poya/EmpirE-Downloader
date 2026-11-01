
import asyncio
import logging
from pathlib import Path

import yt_dlp

from config import DOWNLOAD_DIR, MAX_FILE_SIZE_MB


logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """Raised when a download fails."""


def _download_sync(url: str) -> str:
    """Download media using yt-dlp."""

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    options = {
        "format": "best[ext=mp4]/best",
        "outtmpl": str(DOWNLOAD_DIR / "%(title).100s.%(ext)s"),
        "noplaylist": True,
        "max_filesize": MAX_FILE_SIZE_MB * 1024 * 1024,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=True)
            file_path = downloader.prepare_filename(info)

        path = Path(file_path)

        if not path.exists():
            raise DownloadError("Downloaded file was not found.")

        if path.stat().st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            path.unlink(missing_ok=True)
            raise DownloadError(
                f"File exceeds the {MAX_FILE_SIZE_MB} MB limit."
            )

        return str(path)

    except DownloadError:
        raise
    except Exception as error:
        logger.exception("Download failed.")
        raise DownloadError(
            "Unable to download this link."
        ) from error


async def download_media(url: str) -> str:
    """Download media without blocking the bot event loop."""

    if not url or not url.startswith(("http://", "https://")):
        raise DownloadError(
            "Please provide a valid HTTP or HTTPS link."
        )

    try:
        return await asyncio.to_thread(_download_sync, url)

    except DownloadError:
        raise
    except Exception as error:
        logger.exception("Unexpected download error.")
        raise DownloadError(
            "An unexpected download error occurred."
        ) from error


import logging
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, LOG_LEVEL, DOWNLOAD_DIR
from downloader.engine import DownloadError, download_media


logger = logging.getLogger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle the /start command."""

    welcome_message = (
        "Welcome to EmpirE Downloader! 🚀\n\n"
        "به امپایر دانلودر خوش آمدید! 🚀\n\n"
        "Send a link to start downloading.\n"
        "برای شروع دانلود، لینک موردنظرت را ارسال کن."
    )

    if update.message:
        await update.message.reply_text(welcome_message)


async def handle_link(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle links sent by users."""

    if not update.message or not update.message.text:
        return

    url = update.message.text.strip()

    status_message = await update.message.reply_text(
        "⏳ Downloading... Please wait.\n"
        "⏳ در حال دانلود... لطفاً صبر کن."
    )

    file_path = None

    try:
        file_path = await download_media(url)

        await status_message.edit_text(
            "📤 Download completed. Sending your file...\n"
            "📤 دانلود تمام شد. در حال ارسال فایل..."
        )

        with open(file_path, "rb") as media_file:
            await update.message.reply_document(
                document=media_file,
                filename=Path(file_path).name,
                read_timeout=120,
                write_timeout=120,
                connect_timeout=30,
            )

        await status_message.edit_text(
            "✅ Done!\n"
            "✅ انجام شد!"
        )

    except DownloadError as error:
        await status_message.edit_text(
            f"❌ Download failed:\n{error}\n\n"
            "❌ دانلود ناموفق بود."
        )

    except Exception:
        logger.exception("Error while processing user link.")

        await status_message.edit_text(
            "❌ Something went wrong while sending the file.\n"
            "❌ هنگام ارسال فایل مشکلی پیش آمد."
        )

    finally:
        if file_path:
            try:
                download_path = Path(file_path).resolve()
                download_dir = DOWNLOAD_DIR.resolve()

                if download_path.is_relative_to(download_dir):
                    download_path.unlink(missing_ok=True)
                else:
                    logger.error(
                        "Refusing to delete file outside download directory: %s",
                        download_path,
                    )

            except OSError:
                logger.exception("Failed to remove downloaded file.")


def build_application():
    """Create and configure the Telegram bot application."""

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing. Check your environment variables."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
    )

    return application


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    )

    logging.info("EmpirE Downloader is starting...")

    application = build_application()
    application.run_polling()


if __name__ == "__main__":
    main()

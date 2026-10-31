
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle the /start command."""

    welcome_message = (
        "Welcome to EmpirE Downloader! 🚀\n\n"
        "به امپایر دانلودر خوش آمدید! 🚀\n\n"
        "Send a link to start downloading."
    )

    await update.message.reply_text(welcome_message)


def build_application():
    """Create and configure the Telegram bot application."""

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing. Check your environment variables."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    return application

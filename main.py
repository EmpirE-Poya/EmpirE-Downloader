
import logging

from bot.application import build_application
from config import LOG_LEVEL


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

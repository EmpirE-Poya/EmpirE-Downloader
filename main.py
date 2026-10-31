"""
EmpirE Downloader
Main entry point
"""

import logging


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("EmpirE Downloader is starting...")
    print("EmpirE Downloader - Project initialized!")


if __name__ == "__main__":
    main()
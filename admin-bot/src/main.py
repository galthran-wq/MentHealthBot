import os
import sys
import logging
from decouple import config
from telegram.ext import Updater
from handlers import setup_handlers

def main() -> None:
    token = config("BOT_TOKEN")
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("./logs/log")]
    )
    logging.info("Bot token loaded from configuration")

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    logging.info("Updater and dispatcher initialized")

    setup_handlers(dispatcher)
    logging.info("Handlers set up successfully")

    logging.info("Log directory created or verified")

    logging.info("Logging configured")

    logging.info("Starting admin bot")
    updater.start_polling()
    logging.info("Admin bot is now polling for updates")

    updater.idle()
    logging.info("Admin bot stopped")

if __name__ == '__main__':
    main()

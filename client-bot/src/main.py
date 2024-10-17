import os
import sys
import logging
from datetime import time, timedelta
from decouple import config
from telegram.ext import Updater
from handlers import HANDLERS
from notifications.new_appeals import new_appeals_notify

def main() -> None:
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("./logs/log")]
    )
    logging.info("Logging configured")

    logging.info("Starting client bot")
    
    token = config("BOT_TOKEN")
    prod = config("PROD")
    logging.info(f"Bot token and production flag loaded. Production mode: {prod}")

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue
    logging.info("Updater, dispatcher, and job queue initialized")

    for handler in HANDLERS:
        dispatcher.add_handler(handler)
    logging.info(f"Added {len(HANDLERS)} handlers to the dispatcher")

    job_queue.run_repeating(
        new_appeals_notify,
        timedelta(hours=12),
        time(hour=8-3)  # -3 because of Moscow timezone UTC+3
    )
    logging.info("Scheduled new appeals notification job")

    logging.info("Log directory created or verified")

    updater.start_polling()
    logging.info("Client bot is now polling for updates")

    updater.idle()
    logging.info("Client bot stopped")

if __name__ == '__main__':
    main()

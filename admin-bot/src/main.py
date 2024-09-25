import os
import sys
import logging
from decouple import config
from telegram.ext import Updater
from handlers import HANDLERS

if __name__ == '__main__':
    token = config("BOT_TOKEN")

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    for handler in HANDLERS:
        dispatcher.add_handler(handler)

    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("./logs/log")]
    )

    updater.start_polling()

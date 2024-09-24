from decouple import config
from telegram.ext import Updater
from handlers import HANDLERS

if __name__ == '__main__':
    token = config("BOT_TOKEN")

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    for handler in HANDLERS:
        dispatcher.add_handler(handler)

    updater.start_polling()

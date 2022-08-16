from decouple import config
from telegram.ext import Updater
from handlers import HANDLERS

if __name__ == '__main__':
    token = config("BOT_TOKEN")
    webhook_url = config("WEBHOOK_DOMAIN")
    webhook_port = config("WEBHOOK_PORT")
    prod = config("PROD")

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    for handler in HANDLERS:
        dispatcher.add_handler(handler)

    if prod == "PROD":
        updater.start_webhook(
            listen="0.0.0.0",
            port=webhook_port,
            url_path=token,
            webhook_url=webhook_url + token,
            max_connections=100,
        )
    else:
        updater.start_polling()

    updater.idle()

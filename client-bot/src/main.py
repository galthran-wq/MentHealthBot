from datetime import time, timedelta
from decouple import config
from telegram.ext import Updater
from handlers import HANDLERS
from notifications.new_appeals import new_appeals_notify

if __name__ == '__main__':
    token = config("BOT_TOKEN")
    webhook_url = config("WEBHOOK_DOMAIN")
    webhook_port = config("WEBHOOK_PORT")
    prod = config("PROD")

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue
    for handler in HANDLERS:
        dispatcher.add_handler(handler)
    job_queue.run_repeating(
        new_appeals_notify,
        timedelta(hours=12),
        # -3 because of Moscow timezone UTC+3
        time(hour=8-3)
    )

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

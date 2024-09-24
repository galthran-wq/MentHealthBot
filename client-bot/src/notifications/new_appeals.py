from telegram import ParseMode
from telegram.ext import CallbackContext
from utils.get_all_doctors import get_all_doctors
from utils.get_new_appeals import get_new_appeals
from .message_templates.new_appeals_message import NEW_APPEALS_MESSAGE


def new_appeals_notify(context: CallbackContext):
    new_appeals = get_new_appeals()
    number_of_appeals = len(new_appeals)
    if number_of_appeals:
        doctor_ids = get_all_doctors()
        for doctor in doctor_ids:
            context.bot.send_message(
                chat_id=doctor,
                text=NEW_APPEALS_MESSAGE.format(number_of_appeals),
                parse_mode=ParseMode.HTML
            )

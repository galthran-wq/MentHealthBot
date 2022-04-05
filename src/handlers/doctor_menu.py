from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.find_appeals_by_doctor_id import find_appeals_by_doctor_id
from utils.find_user import find_user
from utils.get_new_appeals import get_new_appeals


def doctor_menu(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)

    new_appeals = len(get_new_appeals())
    doctor_appeals = len(find_appeals_by_doctor_id(user))

    buttons = [InlineKeyboardButton(
                text=f"Новые заявки ({new_appeals})",
                callback_data="new_appeals_menu_button"
               )]
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text="Главное меню",
        reply_markup=kb
    )

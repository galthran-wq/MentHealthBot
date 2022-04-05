from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.find_user import find_user
from utils.get_new_appeals import get_new_appeals


def make_keyboard():
    new_appeals = get_new_appeals()
    buttons = [
        InlineKeyboardButton(text=appeal[0], 
                             callback_data=f"get_appeal_{appeal[1]}_button") 
        for appeal in new_appeals
    ]
    buttons.append(InlineKeyboardButton(text="В главное меню", 
                                        callback_data="doctor_menu_button"))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    return kb

def doctor_select_appeal(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    print(user.state)

    kb = make_keyboard()

    context.bot.send_message(
        chat_id=telegram_user.id,
        text="Нажмите на заявку, чтобы ознакомиться с кейсом",
        reply_markup=kb
    )

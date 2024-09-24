from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from states import UserStates
from utils.check_state import check_state
from utils.find_user import find_user
from utils.get_new_appeals import get_new_appeals
from utils.update_user_state import update_user_state


def make_keyboard() -> InlineKeyboardMarkup:
    new_appeals = get_new_appeals()
    buttons = []
    for appeal in new_appeals:
        name_and_conn = appeal[0]
        conncetion = appeal[1]
        buttons.append(InlineKeyboardButton(
            text=name_and_conn,
            callback_data=f"get_appeal_{conncetion}_button"))
    buttons.append(InlineKeyboardButton(text="В главное меню",
                                        callback_data="doctor_menu_button"))
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    return kb


def doctor_select_appeal(update: Update, context: CallbackContext):
    update.callback_query.answer()
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.DOCTOR_MENU_STATE,
                             UserStates.EXAMINE_APPEAL_STATE])

    kb = make_keyboard()

    context.bot.send_message(
        chat_id=telegram_user.id,
        text="Нажмите на заявку, чтобы ознакомиться с кейсом",
        reply_markup=kb
    )

    update_user_state(user, UserStates.SELECT_APPEAL_STATE)

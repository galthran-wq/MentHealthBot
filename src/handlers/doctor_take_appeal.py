from re import search
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from states import UserStates
from utils.check_state import check_state
from utils.find_appeal_by_id import find_appeal_by_id
from utils.find_user import find_user
from utils.find_user_by_id import find_user_by_id
from utils.update_user_state import update_user_state
from .message_templates.doctor_take_appeal_message import MESSAGE


def make_keyboard() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(
        text=f"Спасибо, господин Xi! 🍚",
        callback_data="doctor_menu_button"
    )]
    kb = InlineKeyboardMarkup([[*buttons]])
    return kb


def doctor_take_appeal(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    user = find_user(telegram_user)
    check_state(user.state, [UserStates.EXAMINE_APPEAL_STATE])
    update_user_state(user, UserStates.TAKE_APPEAL_STATE)
    
    appeal_id = search(r"(?P<id>\d+)", update.callback_query.data)
    appeal_id = appeal_id.group("id")
    appeal = find_appeal_by_id(appeal_id)
    appeal.update(therapist_id=user.id).execute()
    appeal.update(active=False).execute()
    patient = find_user_by_id(appeal.patient_id)

    kb = make_keyboard()
    
    context.bot.send_message(
        chat_id=telegram_user.id,
        text=MESSAGE.format(patient.last_name, patient.first_name, patient.telegram_username),
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )

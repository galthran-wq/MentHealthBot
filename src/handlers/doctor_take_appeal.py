from re import search
from models import Appeal, User
from states import UserStates
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from utils.check_state import check_state
from utils.find_appeal_by_id import find_appeal_by_id
from utils.find_user import find_user
from utils.find_user_by_id import find_user_by_id
from utils.update_user_state import update_user_state
from .message_templates.doctor_take_appeal_message import MESSAGE
from .message_templates.finish_conversation_message import \
    FINISH_CONVERSATION_MESSAGE_WITH_THERAPIST


def update_appeal(appeal_id: int, therapist: User) -> Appeal:
    appeal = find_appeal_by_id(appeal_id)
    appeal.therapist = therapist.id
    appeal.active = False
    appeal.save(only=[Appeal.therapist, Appeal.active])
    return appeal


def send_notification(user: User, therapist: User, context: CallbackContext):
    buttons = [InlineKeyboardButton(
        text="Поделиться проблемой",
        callback_data="create_appeal_button"
    )]
    kb = InlineKeyboardMarkup([[*buttons]])
    context.bot.send_message(
        chat_id=user.telegram_id,
        text=FINISH_CONVERSATION_MESSAGE_WITH_THERAPIST.format(
            therapist.telegram_username),
        reply_markup=kb
    )


def make_keyboard() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(
        text="Спасибо, господин Xi! 🍚",
        callback_data="doctor_menu_button"
    )]
    kb = InlineKeyboardMarkup([[*buttons]])
    return kb


def doctor_take_appeal(update: Update, context: CallbackContext):
    telegram_user = update.effective_user
    therapist = find_user(telegram_user)
    check_state(therapist.state, [UserStates.EXAMINE_APPEAL_STATE])
    update_user_state(therapist, UserStates.TAKE_APPEAL_STATE)

    appeal_id = search(r"(?P<id>\d+)", update.callback_query.data)
    appeal_id = appeal_id.group("id")
    appeal = update_appeal(appeal_id, therapist)
    patient = find_user_by_id(appeal.patient_id)
    send_notification(patient, therapist, context)

    kb = make_keyboard()
    context.bot.send_message(
        chat_id=telegram_user.id,
        text=MESSAGE.format(patient.first_name,
                            patient.last_name, patient.telegram_username),
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )

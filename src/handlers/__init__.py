from filters.state_filter import StateFilter
from .check_authorization_callback import check_authorization_callback
from states import UserStates
from .user_welcome_callback import user_welcome_callback
from .authorized_user_callback import authorized_user_callback
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler

HANDLERS = [
    CommandHandler("start", user_welcome_callback),
    MessageHandler(
        StateFilter(UserStates.AWAITING_AUTHORIZATION_STATE),
        check_authorization_callback
    ),
    MessageHandler(
        StateFilter(UserStates.DOCTOR_MENU_STATE), authorized_user_callback
    ),
    MessageHandler(
        StateFilter(UserStates.SELECT_PROBLEM_STATE), authorized_user_callback
    )
]

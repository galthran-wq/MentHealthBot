from filters.state_filter import StateFilter
from .check_authorization_callback import check_authorization_callback
from states import UserStates
from .user_welcome_callback import user_welcome_callback
from .authorized_user_callback import authorized_user_callback
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler

HANDLERS = [
    CommandHandler("start", user_welcome_callback),
    CallbackQueryHandler("auth_succesfull", authorized_user_callback),
]

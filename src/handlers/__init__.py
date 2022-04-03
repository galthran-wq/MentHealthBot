from filters.state_filter import StateFilter
from .check_authorization_callback import check_authorization_callback
from states import UserStates
from .user_welcome_callback import user_welcome_callback
from .select_problem_state_callback import select_problem_callback
from .change_problem_callback import change_problem_callback
from .done_problem_selecting_callback import done_problem_selecting_callback
from .authorized_user_callback import authorized_user_callback
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler

HANDLERS = [
    CommandHandler("start", user_welcome_callback),
    CallbackQueryHandler("auth_succesfull", authorized_user_callback),
    CallbackQueryHandler(
        change_problem_callback,
        pattern=r".*_problem_button$"
    ),
    CallbackQueryHandler(
        done_problem_selecting_callback,
        pattern=r"^done_selecting_problems_button$"
    )
]

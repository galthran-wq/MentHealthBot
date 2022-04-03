from filters.state_filter import StateFilter
from .check_authorization_callback import check_authorization_callback
from states import UserStates
from .user_welcome_callback import user_welcome_callback
from .select_problem_state_callback import done_problem_selecting_callback, select_problem_callback, change_problem_callback
from .add_custom_problem_callback import add_custom_problem_callback
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
    ),
    CallbackQueryHandler(
        change_problem_callback,
        pattern=r".*_problem_button$"
    ),
    CallbackQueryHandler(
        done_problem_selecting_callback,
        pattern=r"^done_selecting_problems_button$"
    ),
    # MessageHandler(
    #     StateFilter(UserStates.ADD_PROBLEM_STATE), add_custom_problem_callback
    # )
]

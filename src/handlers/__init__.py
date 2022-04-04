from filters.state_filter import StateFilter
from .check_authorization_callback import check_authorization_callback
from states import UserStates
from .user_welcome_callback import user_welcome_callback
from .select_problem_state_callback import select_problem_callback
from .change_problem_callback import change_problem_callback
from .done_problem_selecting_callback import done_problem_selecting_callback
from .authorized_user_callback import authorized_user_callback
from .user_selection_language_callback import user_selection_language_callback
from .select_connection_callback import select_connection_callback
from .select_problem_state_callback import select_problem_callback
from .public_awaiting_approve_callback import public_awaiting_approve_callback
from .finish_conversation_callback import finish_conversation_callback
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler

HANDLERS = [
    CommandHandler("start", select_problem_callback),

    CallbackQueryHandler(authorized_user_callback, pattern="auth_succesfull"),
    MessageHandler(
        StateFilter(UserStates.AWAITING_AUTHORIZATION_STATE),
        authorized_user_callback
    ),

    CallbackQueryHandler(select_connection_callback, pattern="russia"),
    CallbackQueryHandler(select_connection_callback, pattern="english"),

    CallbackQueryHandler(public_awaiting_approve_callback, pattern="personal"),
    CallbackQueryHandler(public_awaiting_approve_callback, pattern="online"),
    CallbackQueryHandler(public_awaiting_approve_callback, pattern="chat"),

    # ToDo: If the user don't click to good_button???
    CallbackQueryHandler(finish_conversation_callback, pattern="good"),

    CallbackQueryHandler(select_problem_callback, pattern="problem_button"),
    CallbackQueryHandler(select_problem_callback, pattern="share_problem"),

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
        user_selection_language_callback,
        pattern=r"^done_selecting_problems_button$"
    )
]

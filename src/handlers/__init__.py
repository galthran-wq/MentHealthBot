from filters.state_filter import StateFilter
from states import UserStates
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler

from handlers.doctor_menu_state import doctor_menu_callback

from .authorized_user_callback import authorized_user_callback
from .change_problem_callback import change_problem_callback
from .check_authorization_callback import check_authorization_callback
from .doctor_examine_apeal_state import doctor_examine_appeal
from .doctor_menu_state import doctor_menu_callback
from .doctor_select_appeal_state import doctor_select_appeal
from .finish_conversation_callback import finish_conversation_callback
from .public_awaiting_approve_callback import public_awaiting_approve_callback
from .select_connection_callback import select_connection_callback
from .select_problem_state_callback import select_problem_callback
from .user_selection_language_callback import user_selection_language_callback
from .user_welcome_callback import user_welcome_callback

HANDLERS = [
    CommandHandler(
        "start",
        user_welcome_callback
    ),

    # todo: change name of the button after @olex1313 will set up authorization server
    CallbackQueryHandler(
        authorized_user_callback,
        pattern="auth_succesfull"
    ),

    MessageHandler(
        StateFilter(UserStates.AWAITING_AUTHORIZATION_STATE),
        authorized_user_callback
    ),

    MessageHandler(
        StateFilter(UserStates.DOCTOR_MENU_STATE),
        authorized_user_callback
    ),

    MessageHandler(
        StateFilter(UserStates.SELECT_PROBLEM_STATE),
        authorized_user_callback
    ),

    # user can reach this step with two ways: when he/she registers in the bot
    # and when he/she wants to share the problem again
    CallbackQueryHandler(
        select_problem_callback,
        pattern=r"^create_appeal_button$"
    ),

    CallbackQueryHandler(
        change_problem_callback,
        pattern=r".+_problem_button$"
    ),

    CallbackQueryHandler(
        user_selection_language_callback,
        pattern=r"^done_selecting_problems_button$"
    ),

    CallbackQueryHandler(
        select_connection_callback,
        pattern=r"set_.+_lang_button"
    ),

    CallbackQueryHandler(
        public_awaiting_approve_callback,
        pattern=r".+_connection_type_button"
    ),

    # ToDo: If the user don't click to good_button???
    CallbackQueryHandler(
        finish_conversation_callback,
        pattern=r"^cancel_appeal_button$"
    ),

    CallbackQueryHandler(
        doctor_menu_callback,
        pattern=r"^doctor_menu_button$"
    ),

    CallbackQueryHandler(
        doctor_select_appeal,
        pattern=r"^new_appeals_menu_button$"
    ),

    CallbackQueryHandler(
        doctor_examine_appeal,
        pattern=r"^get_appeal_.*_button$"
    )
]

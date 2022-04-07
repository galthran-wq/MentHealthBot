from filters.state_filter import StateFilter
from states import UserStates
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler

from .all_welcome import all_welcome
from .authorized_user_router import authorized_user_router
from .check_authorization import check_authorization
from .doctor_examine_appeal import doctor_examine_appeal
from .doctor_menu import doctor_menu
from .doctor_select_appeal import doctor_select_appeal
from .doctor_take_appeal import doctor_take_appeal
from .user_change_problem import user_change_problem
from .user_finish_conversation import user_finish_conversation
from .user_public_awaiting_approve import user_public_awaiting_approve
from .user_select_connection import user_select_connection
from .user_select_language import user_select_language
from .user_select_problem import user_select_problem

HANDLERS = [
    CommandHandler(
        "start",
        all_welcome
    ),

    # todo: change name of the button after @olex1313 will set up authorization server
    CallbackQueryHandler(
        authorized_user_router,
        pattern="auth_succesfull"
    ),

    MessageHandler(
        StateFilter(UserStates.AWAITING_AUTHORIZATION_STATE),
        authorized_user_router
    ),

    MessageHandler(
        StateFilter(UserStates.DOCTOR_MENU_STATE),
        authorized_user_router
    ),

    MessageHandler(
        StateFilter(UserStates.SELECT_PROBLEM_STATE),
        authorized_user_router
    ),

    # user can reach this step with two ways: when he/she registers in the bot
    # and when he/she wants to share the problem again
    CallbackQueryHandler(
        user_select_problem,
        pattern=r"^create_appeal_button$"
    ),

    CallbackQueryHandler(
        user_change_problem,
        pattern=r".+_problem_button$"
    ),

    CallbackQueryHandler(
        user_select_language,
        pattern=r"^done_selecting_problems_button$"
    ),

    CallbackQueryHandler(
        user_select_connection,
        pattern=r"set_.+_lang_button"
    ),

    CallbackQueryHandler(
        user_public_awaiting_approve,
        pattern=r".+_connection_type_button"
    ),

    # ToDo: If the user don't click to cancel_appeal_button???
    CallbackQueryHandler(
        user_finish_conversation,
        pattern=r"^cancel_appeal_button$"
    ),

    CallbackQueryHandler(
        doctor_menu,
        pattern=r"^doctor_menu_button$"
    ),

    CallbackQueryHandler(
        doctor_select_appeal,
        pattern=r"^new_appeals_menu_button$"
    ),

    CallbackQueryHandler(
        doctor_examine_appeal,
        pattern=r"^get_appeal_.+_button$"
    ),

    CallbackQueryHandler(
        doctor_take_appeal,
        pattern=r"^take_appeal_.+_button$"
    )
]

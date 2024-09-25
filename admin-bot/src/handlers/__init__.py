from .welcome_message import welcome_message
from .add_doctor import add_doctor_start, add_doctor
from .delete_doctor import delete_doctor_start, delete_doctor
from .doctor_list import doctor_list
from .add_admin import add_admin, add_admin_start
from .delete_admin import delete_admin, delete_admin_start
from .admin_list import admin_list
from .back import back
from .help import help
from .authorization_state import authorization_state
from filters.state_filter import StateFilter
from states import UserStates
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler

HANDLERS = [
    CommandHandler(
        "start",
        welcome_message
    ),
    CommandHandler(
        'back',
        back
    ),
    CommandHandler(
        'help',
        help
    ),
    CommandHandler(
        'add_doctor',
        add_doctor_start
    ),
    MessageHandler(
        StateFilter(UserStates.ADD_DOCTOR_STATE),
        add_doctor
    ),
    CommandHandler(
        'delete_doctor',
        delete_doctor_start
    ),
    MessageHandler(
        StateFilter(UserStates.DELETE_DOCTOR_STATE),
        delete_doctor
    ),
    CommandHandler(
        'doctor_list',
        doctor_list
    ),
    MessageHandler(
        StateFilter(UserStates.ADD_ADMIN_STATE),
        add_admin
    ),
    CommandHandler(
        'add_admin',
        add_admin_start
    ),
    MessageHandler(
        StateFilter(UserStates.DELETE_ADMIN_STATE),
        delete_admin
    ),
    CommandHandler(
        'delete_admin',
        delete_admin_start
    ),
    CommandHandler(
        'admin_list',
        admin_list
    )
]

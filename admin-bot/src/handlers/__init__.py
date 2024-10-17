import logging
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
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler

def setup_handlers(application: Application) -> None:
    logging.info("Setting up handlers for admin bot")
    
    handlers = [
        ("start", welcome_message, "command"),
        ("back", back, "command"),
        ("help", help, "command"),
        ("add_doctor", add_doctor_start, "command"),
        (UserStates.ADD_DOCTOR_STATE, add_doctor, "state"),
        ("delete_doctor", delete_doctor_start, "command"),
        (UserStates.DELETE_DOCTOR_STATE, delete_doctor, "state"),
        ("doctor_list", doctor_list, "command"),
        (UserStates.ADD_ADMIN_STATE, add_admin, "state"),
        ("add_admin", add_admin_start, "command"),
        (UserStates.DELETE_ADMIN_STATE, delete_admin, "state"),
        ("delete_admin", delete_admin_start, "command"),
        ("admin_list", admin_list, "command")
    ]
    
    for handler in handlers:
        name, func, handler_type = handler
        if handler_type == "command":
            application.add_handler(CommandHandler(name, func))
            logging.info(f"Added command handler: {name}")
        elif handler_type == "state":
            application.add_handler(MessageHandler(StateFilter(name), func))
            logging.info(f"Added state handler: {name}")
    
    logging.info("Handlers setup completed for admin bot")

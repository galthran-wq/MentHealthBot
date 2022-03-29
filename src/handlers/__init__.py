from .user_welcome_callback import user_welcome_callback
from telegram.ext import CommandHandler

HANDLERS = [
CommandHandler("start", user_welcome_callback)
]
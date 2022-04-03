from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from .message_templates.add_custom_problem_message import ADD_CUSTOM_PROBLEM_MESSAGE
from states import UserStates
from utils.find_or_create_user import find_or_create_user

def add_custom_problem_callback(update: Update, context: CallbackContext):
    #todo: this function is undone 
    telegram_user = update.effective_user
    user = find_or_create_user(telegram_user)

    user.state = UserStates.ADD_PROBLEM_STATE
    user.save()
    
    button = InlineKeyboardButton(text="Назад", callback_data="back_button")
    kb = InlineKeyboardMarkup([[button]])

    context.bot.send_message(
        chat_id=telegram_user.id,
        text=ADD_CUSTOM_PROBLEM_MESSAGE,
        reply_markup=kb
    )

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from .message_templates.are_you_hse_student_message import ARE_YOU_HSE_STUDENT_MESSAGE, NOT_HSE_STUDENT_MESSAGE
from utils.update_user_state import update_user_state
from utils.find_user import find_user
from states import UserStates
from handlers.user_select_problem import user_select_problem

def ask_if_hse_student(update: Update, context: CallbackContext):
    buttons = [
        InlineKeyboardButton(text="Да", callback_data="hse_student_yes"),
        InlineKeyboardButton(text="Нет", callback_data="hse_student_no")
    ]
    kb = InlineKeyboardMarkup([[btn] for btn in buttons])
    
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=ARE_YOU_HSE_STUDENT_MESSAGE,
        reply_markup=kb
    )

def handle_hse_student_response(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "hse_student_yes":
        user_select_problem(update, context)
    else:
        # Send a message for non-HSE students
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=NOT_HSE_STUDENT_MESSAGE
        )
        update_user_state(find_user(update.effective_user), UserStates.FINISH_CONVERSATION_STATE) 
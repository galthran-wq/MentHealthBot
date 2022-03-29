from telegram import (
    Update,
)
from telegram.ext import (
    CallbackContext,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
)
from models.models import User, Message
from utils import log_out_msg, log_in_update
from user_states import UserStates
from filters import StateFilter


def help_me_message_callback(update: Update, context: CallbackContext):
    uid = update.effective_user.id

    msg = context.bot.send_message(chat_id=uid,
                                   text="Как дела? Напиши")

    user = User.select().where(User.telegram_id == uid).get()

    log_out_msg(msg, user)
    log_in_update(update, user)

    user.state = UserStates.HOW_ARE_YOU
    user.save()


help_me_message_handler = CallbackQueryHandler(
    callback=help_me_message_callback,
    pattern="help_me"
)


def auth_message_callback(update: Update, context: CallbackContext):
    uid = update.effective_user.id

    msg = context.bot.send_message(chat_id=uid,
                                   text="Написано же, не работает... Как зовут?")

    user = User.select().where(User.telegram_id == uid).get()

    log_out_msg(msg, user)
    log_in_update(update, user)

    user.state = UserStates.WHAT_IS_YOUR_NAME
    user.save()


auth_message_handler = CallbackQueryHandler(
    callback=auth_message_callback,
    pattern="fake_auth"
)


def how_are_you_callback(update: Update, context: CallbackContext):
    uid = update.effective_user.id

    msg = context.bot.send_message(chat_id=uid,
                                   text="Окей, понял. Сяп.")
    context.bot.edit_message_reply_markup(chat_id=uid,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=None)
    user = User.select().where(User.telegram_id == uid).get()

    log_out_msg(msg, user)
    log_in_update(update, user)

    user.state = UserStates.FINAL
    user.save()


how_are_you_handler = MessageHandler(
    callback=how_are_you_callback,
    filters=StateFilter(UserStates.HOW_ARE_YOU)
)


def what_is_your_name_callback(update: Update, context: CallbackContext):
    uid = update.effective_user.id

    msg = context.bot.send_message(chat_id=uid,
                                   text="Окей, понял. Сяп.")

    user = User.select().where(User.telegram_id == uid).get()

    log_out_msg(msg, user)
    log_in_update(update, user)

    user.state = UserStates.FINAL
    user.save()


what_is_your_name_handler = MessageHandler(
    callback=what_is_your_name_callback,
    filters=StateFilter(UserStates.WHAT_IS_YOUR_NAME)
)

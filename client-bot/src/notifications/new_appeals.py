import logging
from telegram import ParseMode
from telegram.ext import CallbackContext
from utils.get_all_doctors import get_all_doctors
from utils.get_new_appeals import get_new_appeals
from .message_templates.new_appeals_message import NEW_APPEALS_MESSAGE


def new_appeals_notify(context: CallbackContext):
    logging.info("Starting new appeals notification process")
    new_appeals = get_new_appeals()
    number_of_appeals = len(new_appeals)
    logging.info(f"Found {number_of_appeals} new appeals")
    
    if number_of_appeals:
        doctor_ids = get_all_doctors()
        logging.info(f"Retrieved {len(doctor_ids)} doctor IDs for notification")
        
        successful_notifications = 0
        failed_notifications = 0
        
        for doctor in doctor_ids:
            try:
                context.bot.send_message(
                    chat_id=doctor,
                    text=NEW_APPEALS_MESSAGE.format(number_of_appeals),
                    parse_mode=ParseMode.HTML
                )
                logging.info(f"Notification sent to doctor with ID: {doctor}")
                successful_notifications += 1
            except Exception as e:
                logging.error(f"Failed to send notification to doctor with ID: {doctor}. Error: {str(e)}")
                failed_notifications += 1
        
        logging.info(f"Notification process completed. Successful: {successful_notifications}, Failed: {failed_notifications}")
    else:
        logging.info("No new appeals found, skipping notifications")

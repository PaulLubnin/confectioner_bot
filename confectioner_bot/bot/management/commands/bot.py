import os
from dotenv import load_dotenv

from django.core.management.base import BaseCommand

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, LabeledPrice
from telegram import PreCheckoutQuery
from telegram import error as telegram_error
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
    PreCheckoutQueryHandler,
)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте. Это бот по заказу тортов"
    )


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()
        tg_token = os.getenv("TG_BOT_TOKEN")
        updater = Updater(tg_token)
        dispatcher = updater.dispatcher
        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)        

        
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    Command().handle()

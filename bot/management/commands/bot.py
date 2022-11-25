import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Updater,
)

from bot.bot_handlers import (
    CAKES, CAKE, QUIT_MENU, MAIN_MENU, ONE, TWO, THREE, FOUR, FIVE, CUSTOM_CAKES, CUSTOM_CAKE, start, start_over, end,
    cakes, custom_cakes,
)


class Command(BaseCommand):
    help = 'Запуск чат-бота'

    def handle(self, *args, **options):
        load_dotenv()

        tg_token = os.getenv("TG_BOT_TOKEN")
        updater = Updater(tg_token)
        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                CAKES: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(THREE) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(FOUR) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(FIVE) + '$'),
                ],
                CUSTOM_CAKES: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(THREE) + '$'),
                ],
                MAIN_MENU: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(cakes, pattern='^' + str(CAKE) + '$'),
                    CallbackQueryHandler(custom_cakes, pattern='^' + str(CUSTOM_CAKE) + '$'),
                ],
            },
            fallbacks=[CommandHandler('start', start)],
        )
        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()

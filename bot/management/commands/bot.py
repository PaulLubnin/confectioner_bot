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
    CAKES, CUSTOM_CAKES, MAIN_MENU, ORDER_MENU, BUCKET_MENU,
    QUIT_MENU, CAKE, CUSTOM_CAKE, REGISTER, PAY, AGREEMENT,
    ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN,
    start, start_over, end,
    cakes, custom_cakes, add_cake_to_order, register, pay, order, agreement
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
                    CallbackQueryHandler(add_cake_to_order, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(add_cake_to_order, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(add_cake_to_order, pattern='^' + str(THREE) + '$'),
                    CallbackQueryHandler(add_cake_to_order, pattern='^' + str(FOUR) + '$'),
                    CallbackQueryHandler(add_cake_to_order, pattern='^' + str(FIVE) + '$'),
                ],
                CUSTOM_CAKES: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(MAIN_MENU) + '$'),
                ],
                MAIN_MENU: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(cakes, pattern='^' + str(CAKE) + '$'),
                    CallbackQueryHandler(custom_cakes, pattern='^' + str(CUSTOM_CAKE) + '$'),
                ],
                BUCKET_MENU: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(MAIN_MENU) + '$'),
                    CallbackQueryHandler(agreement, pattern='^' + str(ORDER_MENU) + '$'),
                ],
                AGREEMENT: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(MAIN_MENU) + '$'),
                    CallbackQueryHandler(order, pattern='^' + str(ORDER_MENU) + '$'),
                ],
                ORDER_MENU: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(register, pattern='^' + str(REGISTER) + '$'),
                    CallbackQueryHandler(pay, pattern='^' + str(PAY) + '$'),
                ],
                REGISTER: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(MAIN_MENU) + '$'),
                ],
                PAY: [
                    CallbackQueryHandler(end, pattern='^' + str(QUIT_MENU) + '$'),
                    CallbackQueryHandler(start_over, pattern='^' + str(MAIN_MENU) + '$'),
                ],
            },
            fallbacks=[CommandHandler('start', start)],
        )
        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()

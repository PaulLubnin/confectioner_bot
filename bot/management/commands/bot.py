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

from bot.models import Cake

# меню
CAKES, CUSTOM_CAKES, MAIN_MENU = range(3)
# Выбор в главном меню
QUIT_MENU, CAKE, CUSTOM_CAKE = range(3)
# Кнопки с нумерацией
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(10)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
#    breakpoint()
    print(f"User {user.first_name} started the conversation.")
    keyboard = [
        [
            InlineKeyboardButton("Выбрать торт", callback_data=str(CAKE)),
            InlineKeyboardButton("Конструктор тортов", callback_data=str(CUSTOM_CAKE)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Здравствуйте, {user.first_name}. Это бот по заказу тортов.", reply_markup=reply_markup)
    # Надо сформировать заказ
    return MAIN_MENU


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Выбрать торт", callback_data=str(CAKE)),
            InlineKeyboardButton("Конструктор тортов", callback_data=str(CUSTOM_CAKE)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Надо сформировать заказ
    query.edit_message_text(text="Какой торт вы желаете заказать?", reply_markup=reply_markup)
    return MAIN_MENU


def get_default_cakes():
    default_cakes = {}
    num = 1
    for cake in Cake.objects.filter(default=True):
        default_cakes[num] = {
            'description': cake.description,
            'price': cake.get_price(),
            'image': cake.picture,
        }
        num += 1
    return default_cakes


def cakes(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    cake_catalogue = get_default_cakes()

    query = update.callback_query
    query.answer()
    bot = query.bot
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ],
        [
            InlineKeyboardButton("4", callback_data=str(FOUR)),
            InlineKeyboardButton("5", callback_data=str(FIVE)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(query.from_user.id, text="Популярные торты:")

    for key, value in cake_catalogue.items():
#        breakpoint()
        bot.send_message(query.from_user.id, text=f"{key}. {value['description']}")
        bot.send_message(query.from_user.id, text=f"Цена: {str(value['price'])} руб.")
        bot.send_photo(query.from_user.id, photo=value['image'])            
    
    bot.send_message(
        query.from_user.id, 
        text="Выберите торт:", 
        reply_markup=reply_markup
    )

    return CAKES


def custom_cakes(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str('TWO')),
            InlineKeyboardButton("3", callback_data=str('THREE')),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return CUSTOM_CAKES


def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="До встречи!")
    return ConversationHandler.END


def cake_bot():
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


if __name__ == "__main__":
    cake_bot()

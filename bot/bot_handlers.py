from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

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
    # breakpoint()
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
        # breakpoint()
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

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.models import Cake

# меню
CAKES, CUSTOM_CAKES, MAIN_MENU, ORDER_MENU, BUCKET_MENU, REGISTER, PAY = range(7)
AGREEMENT = 98
QUIT_MENU = 99
# Выбор в главном меню
CAKE, CUSTOM_CAKE = range(2)
# Кнопки с нумерацией
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(10)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
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
    query.edit_message_text(text="Какой торт вы желаете заказать?", reply_markup=reply_markup)
    return MAIN_MENU


def get_default_cakes():
    default_cakes = {}
    num = 1
    for cake in Cake.objects.filter(default=True):
        default_cakes[num] = {
            "title": cake.title,
            "price": cake.get_price(),
            "picture": cake.picture,
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
        bot.send_photo(
            query.from_user.id, 
            photo=value["picture"],
            caption=f"{key}. {value['title']} \nЦена: {str(value['price'])} руб."
            )            
        
    bot.send_message(
        query.from_user.id, 
        text="Выберите торт:", 
        reply_markup=reply_markup
    )

    return CAKES


def add_cake_to_order(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    bot = query.bot
    keyboard = [
        [
            InlineKeyboardButton("Добавить торт", callback_data=str(MAIN_MENU)),
            InlineKeyboardButton("Оформить заказ", callback_data=str(ORDER_MENU)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        query.from_user.id,
        text="Сейчас в вашей корзине: ...",
        reply_markup=reply_markup
    )
    return BUCKET_MENU


def order(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    bot = query.bot
    keyboard = [
        [
            InlineKeyboardButton("Регистрация", callback_data=str(REGISTER)),
            InlineKeyboardButton("Оплатить заказ", callback_data=str(PAY)),
            InlineKeyboardButton("Согласие", callback_data=str(AGREEMENT)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    with open("./confectioner_bot/media/AgreementPD.pdf", "rb") as pd_file:
        bot.send_document(
            query.from_user.id,
            document=pd_file,
            reply_markup=reply_markup,
            caption="Вам необходимо зарегистрироваться и оплатить заказ.\nПри регистрации и/или оформлении заказа вы даете согласие на обработку персональных данных.\nСогласие приложено к сообщению."
        )           
    return ORDER_MENU


def custom_cakes(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Вернуться в главное меню", callback_data=str(MAIN_MENU)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Раздел в разработке, вернитесь в главное меню.", reply_markup=reply_markup
    )
    return CUSTOM_CAKES


def register(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Вернуться в главное меню", callback_data=str(MAIN_MENU)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Раздел в разработке, вернитесь в главное меню.", reply_markup=reply_markup
    )
    return REGISTER


def pay(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Вернуться в главное меню", callback_data=str(MAIN_MENU)),
        ],
        [
            InlineKeyboardButton("Выйти", callback_data=str(QUIT_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Раздел в разработке, вернитесь в главное меню.", reply_markup=reply_markup
    )
    return PAY


def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="До встречи!")
    return ConversationHandler.END

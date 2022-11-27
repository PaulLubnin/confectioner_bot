from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.models import Cake, Order

# меню
CAKES, CUSTOM_CAKES, MAIN_MENU, ORDER_MENU, BUCKET_MENU, REGISTER, PAY = range(7)
QUIT_MENU = 99
# Выбор в главном меню
CAKE, CUSTOM_CAKE = range(2)
# Кнопки с нумерацией
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(10)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    context.chat_data['order'] = {'cakes': []}
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
    for num, cake in enumerate(Cake.objects.filter(default=True)):
        default_cakes[num+1] = {
            "title": cake.title,
            "price": cake.get_price(),
            "picture": cake.picture,
            "cake_id": cake.id,
        }
    return default_cakes


def cakes(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    cake_catalogue = get_default_cakes()
    query = update.callback_query
    query.answer()
    context.chat_data['cakes'] = cake_catalogue
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


def get_bucket_text(order):
    bucket_text = ''
    bucket_total = 0
    for num, item in enumerate(order['cakes']):
        bucket_text += f"{num+1}. Торт '{item['title']}'. Цена: {item['price']} руб.\n"
        bucket_total += item['price']
    bucket_text += f"Итого к оплате: {bucket_total} руб."
    return bucket_text, bucket_total


def add_cake_to_order(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    bot = query.bot
    order = context.chat_data['order']
    cakes = context.chat_data['cakes']
    selected_cake = cakes[int(query.data) + 1]
    order['cakes'].append(selected_cake)
    bucket_text, bucket_total = get_bucket_text(order)
    order['total'] = bucket_total
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
        text=f"Торт '{selected_cake['title']}' добавлен в корзину.\nСейчас в вашей корзине:\n{bucket_text}",
        reply_markup=reply_markup
    )
    return BUCKET_MENU


def save_order(order):
    new_order = Order(client=None, order_price=order['total'])
    new_order.save()
    for cake in order['cakes']:
        cake_obj = Cake.objects.get(pk=cake['cake_id'])
        new_order.cakes.add(cake_obj)
    new_order.save()
    return new_order.id


def delete_order(order):
    order_to_del = Order.objects.get(pk=order['id'])
    '''удаляем заказ'''
    order_to_del.delete()


def order(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    bot = query.bot
    order = context.chat_data['order']
    if order['cakes']:
        order['id'] = save_order(order)
    keyboard = [
        [
            InlineKeyboardButton("Регистрация", callback_data=str(REGISTER)),
            InlineKeyboardButton("Оплатить заказ", callback_data=str(PAY)),
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
        )           
    bot.send_message(
        query.from_user.id,
        text="Вам необходимо зарегистрироваться и оплатить заказ.\nПри регистрации и/или оформлении заказа вы даете согласие на обработку персональных данных.\nСогласие приложено к предыдущему сообщению.",
        reply_markup=reply_markup,
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
    order = context.chat_data['order']
    delete_order(order)
    order = {}
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="До встречи!")
    return ConversationHandler.END

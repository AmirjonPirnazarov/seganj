import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
import re

API_TOKEN = '7836300949:AAG3XWsj2pJYPXg0GPaOrsF_DxGD1sGevnk'
bot = telebot.TeleBot(API_TOKEN)

connection = mysql.connector.connect(
    host='mysql://root:DvpMLyvpYUWKocjWRnABrIorvfmSsAeA@mysql.railway.internal:3306/railway',
    user='root',
    password='DvpMLyvpYUWKocjWRnABrIorvfmSsAeA',
    database='railway',
    autocommit=True
)
cursor = connection.cursor()

user_data = {}

# Словари с переводами
TEXTS = {
    'ru': {
        'welcome': "Добро пожаловать! \nВыберите язык / \nХуш омадед! \nЗабони худро интихоб намоед:",
        'input_car': "Введите номер вашей машины:",
        'car_not_found': "Ваше авто не найдено в базе. Попробуйте снова или обратитесь на ближайшую АЗС.",
        'no_card': "Пожалуйста, обратитесь на ближайшую АЗС для получения карты или установки приложения SEGANJ.",
        'category': "Ваше авто найдено в базе. Выберите категорию авто:",
        'truck_type': "Выберите тип грузового авто:",
        'fuel': "Выберите вид топлива:",
        'success': "Вы успешно прошли регистрацию! Спасибо!",
        'invalid_format': "Неверный формат номера. Попробуйте снова:",
        'retry': "Попробовать снова"
    },
    'tj': {
        'welcome': "Хуш омадед! Забони худро интихоб намоед:",
        'input_car': "Рақами мошинаи худро ворид кунед (формат: 1234AB56):",
        'car_not_found': "Мошини шумо дар пойгоҳ ефт нашуд. Боз кӯшиш кунед е БА НАЗДИКТАРИН ИСТГОҲИ "
                         "СӮЗИШВОРӢ муроҷиат кунед.",
        'no_card': "Лутфан БАРОИ харита е насби барномаи SEGANJ БА НАЗДИКТАРИН ИСТГОҲИ СӮЗИШВОРӢ муроҷиат кунед.",
        'category': "Мошини шумо дар пойгоҳ ефт шуд. Категорияи мошинро интихоб кунед:",
        'truck_type': "Навъи мошинаи боркашро интихоб кунед:",
        'fuel': "Навъи сӯзишвориро интихоб кунед:",
        'success': "Шумо бо муваффақият сабти ном шудӣ! Ташаккур!",
        'invalid_format': "Формати нодурусти рақам. Боз кӯшиш кунед:",
        'retry': "Боз кӯшиш кунед"
    }
}


def get_text(user_id, key):
    lang = user_data.get(user_id, {}).get('language', 'ru')
    return TEXTS[lang][key]


@bot.message_handler(commands=['start'])
def start_message(message):
    user_data[message.chat.id] = {}
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Русский", callback_data='lang_ru')),
    markup.add(InlineKeyboardButton("Тоҷикӣ", callback_data='lang_tj'))
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите язык / Хуш омадед! Забони худро интихоб намоед:",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language(call):
    lang = call.data.split('_')[1]
    user_data[call.message.chat.id]['language'] = lang
    bot.send_message(call.message.chat.id, get_text(call.message.chat.id, 'input_car'))


def validate_car_number(number):
    pattern = r'^[0-9]{4}[A-ZА-Я]{2}[0-9]{2}$'
    return re.match(pattern, number.upper()) is not None


@bot.message_handler(func=lambda message: message.chat.id in user_data and 'language' in user_data[
    message.chat.id] and 'car_number' not in user_data[message.chat.id])
def check_car_number(message):
    if not validate_car_number(message.text):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(get_text(message.chat.id, 'retry'), callback_data='retry_car'))
        bot.send_message(message.chat.id, get_text(message.chat.id, 'invalid_format'), reply_markup=markup)
        return

    car_number = message.text.upper()
    user_data[message.chat.id]['car_number'] = car_number

    query = "SELECT card_or_app_status, phone_number, full_name, fuel_type FROM users WHERE car_number = %s"
    cursor.execute(query, (car_number,))
    result = cursor.fetchone()

    if result:
        card_or_app_status, phone_number, full_name, fuel_type = result
        user_data[message.chat.id].update({
            'phone_number': phone_number,
            'full_name': full_name,
            'user_fuel_type': fuel_type,
            'card_or_app_status': card_or_app_status
        })

        if card_or_app_status in ['Установлено', 'Карта']:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Легковое ТС", callback_data='cat_car')),
            markup.add(InlineKeyboardButton("Маршрутное такси", callback_data='cat_taxi')),
            markup.add(InlineKeyboardButton("Грузовое ТС", callback_data='cat_truck'))
            bot.send_message(message.chat.id, get_text(message.chat.id, 'category'), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, get_text(message.chat.id, 'no_card'))
            user_data.pop(message.chat.id, None)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(get_text(message.chat.id, 'retry'), callback_data='retry_car'))
        bot.send_message(message.chat.id, get_text(message.chat.id, 'car_not_found'), reply_markup=markup)
        user_data.pop(message.chat.id, None)


@bot.callback_query_handler(func=lambda call: call.data == 'retry_car')
def handle_retry(call):
    # Очищаем данные пользователя для повторной попытки
    user_data[call.message.chat.id] = {
        'language': user_data.get(call.message.chat.id, {}).get('language', 'ru')
    }
    bot.send_message(call.message.chat.id, get_text(call.message.chat.id, 'input_car'))


@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def handle_category(call):
    category = call.data.split('_')[1]
    categories = {
        'car': 'Легковое ТС',
        'taxi': 'Маршрутное такси',
        'truck': 'Грузовое ТС'
    }
    user_data[call.message.chat.id]['car_category'] = categories[category]

    if category == 'truck':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Лабо", callback_data='truck_labo')),
        markup.add(InlineKeyboardButton("Портер", callback_data='truck_porter')),
        markup.add(InlineKeyboardButton("Спринтер", callback_data='truck_sprinter')),
        markup.add(InlineKeyboardButton("Зил", callback_data='truck_zil')),
        markup.add(InlineKeyboardButton("Камаз", callback_data='truck_kamaz')),
        markup.add(InlineKeyboardButton("Дулан", callback_data='truck_dulan'))
        bot.send_message(call.message.chat.id, get_text(call.message.chat.id, 'truck_type'), reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("СУГ/ГАЗ", callback_data='fuel_gas')),
        markup.add(InlineKeyboardButton("Бензин", callback_data='fuel_petrol')),
        markup.add(InlineKeyboardButton("Дизель", callback_data='fuel_diesel'))
        bot.send_message(call.message.chat.id, get_text(call.message.chat.id, 'fuel'), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('truck_'))
def handle_truck_type(call):
    truck_type = call.data.split('_')[1]
    types = {
        'labo': 'Лабо',
        'porter': 'Портер',
        'sprinter': 'Спринтер',
        'zil': 'Зил',
        'kamaz': 'Камаз',
        'dulan': 'Дулан'
    }
    user_data[call.message.chat.id]['truck_type'] = types[truck_type]

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("СУГ/ГАЗ", callback_data='fuel_gas')),
    markup.add(InlineKeyboardButton("Бензин", callback_data='fuel_petrol')),
    markup.add(InlineKeyboardButton("Дизель", callback_data='fuel_diesel'))
    bot.send_message(call.message.chat.id, get_text(call.message.chat.id, 'fuel'), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('fuel_'))
def handle_fuel(call):
    fuel_type = call.data.split('_')[1]
    fuels = {
        'gas': 'СУГ/ГАЗ',
        'petrol': 'Бензин',
        'diesel': 'Дизель'
    }
    user_data[call.message.chat.id]['fuel_type'] = fuels[fuel_type]

    bot.send_message(call.message.chat.id, get_text(call.message.chat.id, 'success'))

    query = """INSERT INTO registrations 
               (chat_id, car_number, car_category, fuel_type, truck_type, 
                phone_number, full_name, user_fuel_type, card_or_app_status) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (
        call.message.chat.id,
        user_data[call.message.chat.id]['car_number'],
        user_data[call.message.chat.id]['car_category'],
        user_data[call.message.chat.id]['fuel_type'],
        user_data[call.message.chat.id].get('truck_type'),
        user_data[call.message.chat.id]['phone_number'],
        user_data[call.message.chat.id]['full_name'],
        user_data[call.message.chat.id]['user_fuel_type'],
        user_data[call.message.chat.id]['card_or_app_status']
    ))
    connection.commit()
    user_data.pop(call.message.chat.id, None)


if __name__ == '__main__':
    bot.polling(none_stop=True)

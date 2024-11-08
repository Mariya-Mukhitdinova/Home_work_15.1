import telebot
import buttons as bt
import database as db
from geopy import Photon

geolocator = Photon(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
bot = telebot.TeleBot(token="7929424594:AAG80zGkZVal2so9Vf6DhUAhZjWK1ArwxSI")
@bot.message_handler(commands=["start"])
def language(message):
    user_id = message.from_user.id
    bot.send_message(user_id,"Выберите язык", reply_markup=bt.lang())
    bot.register_next_step_handler(message, start)
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите своё имя для регистрации")
    bot.send_message(user_id, "Ro'yxatdan o'tish uchun ismingizni kiriting")
    print(message.text)
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    check = db.check_user(user_id)
    if check == True:
        bot.send_message(user_id, f"{name}, Вы уже зарегистрированы!")
        bot.send_message(user_id, f"{name}, Siz allaqachon ro'yxatdan o'tgansiz!")
    elif check == False:
        print(message.text)
        bot.send_message(user_id, f"{name}, Добро пожаловать в бот!", reply_markup=bt.phone_button())
        bot.send_message(user_id, f"{name}, Botga xush kelibsiz!", reply_markup=bt.phone_button())
        # bot.send_message(user_id,  reply_markup=bt.phone_button())
        # bot.send_message(user_id,  reply_markup=bt.phone_button())
        bot.register_next_step_handler(message, get_phone_number, name)

def get_phone_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, f"{name}, Поделитесь своей локацией!", reply_markup=bt.location_button())
        bot.send_message(user_id, f"{name}, Joylashuvingizni baham ko'ring!", reply_markup=bt.location_button())
        bot.register_next_step_handler(message,location, name, phone_number)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку!",  reply_markup=bt.phone_button())
        bot.send_message(user_id, "Raqamingizni tugma orqali yuboring!", reply_markup=bt.phone_button())
        bot.register_next_step_handler(message, get_phone_number,name)


def location(message, name, phone_number):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = geolocator.reverse((latitude,longitude)).address
        print(name, phone_number, address)

        bot.send_message(user_id, "Вы успешно зарегистрировались!")
        bot.send_message(user_id, "Siz ro'yxatdan o'tdingiz!")
        db.add_user(name=name, phone_number=phone_number, user_id=user_id)
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку!", reply_markup=bt.location_button())
        bot.send_message(user_id, "Joylashuvingizni tugma orqali yuboring!", reply_markup=bt.location_button())
        bot.register_next_step_handler(message, location, name, phone_number)


bot.infinity_polling()

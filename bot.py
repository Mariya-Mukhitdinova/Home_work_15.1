import telebot
import buttons as bt
import database as db
from geopy import Photon
import logging
from aiogram import Bot, Dispatcher, executor, types
from translate import Translator

logging.basicConfig(level=logging.INFO)
geolocator = Photon(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
bot = telebot.TeleBot(token="7929424594:AAG80zGkZVal2so9Vf6DhUAhZjWK1ArwxSI")
dp = Dispatcher(bot)

ru_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
uz_letters = "аbdеfghijklmnоpqrstuvxyzoʻgʻshchng"

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id,"Введите своё имя для регистрации")
    print(message.text)
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, f"{name}, Добро пожаловать в бот!")
    check = db.check_user(user_id)
    if check == True:
        bot.send_message(user_id, f"{name}, Вы уже зарегистрированы!")
    elif check == False:
        print(message.text)
        bot.send_message(user_id, f"{name}, Добро пожаловать в бот!")
        bot.send_message(user_id, "Поделитесь своим контактом!", reply_markup=bt.phone_button())
        bot.register_next_step_handler(message, get_phone_number, name)

def get_phone_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, f"{name}, Поделитесь своей локацией!", reply_markup=bt.location_button())
        bot.register_next_step_handler(message,location, name, phone_number)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку!",  reply_markup=bt.phone_button())
        bot.register_next_step_handler(message, get_phone_number,name)


def location(message, name, phone_number):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = geolocator.reverse((latitude,longitude)).address
        print(name, phone_number, address)
        db.add_user(name=name, phone_number=phone_number, user_id=user_id)
        bot.send_message(user_id, "Вы успешно зарегистрировались!", button_translate)

    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку!", reply_markup=bt.location_button())
        bot.register_next_step_handler(message, location, name, phone_number)

@bot.message_handler(commands=['Translator'])
def button_translate(message):
    user_id = message.from_user.id
    bot.send_message(user_id, bt.translate())
    bot.register_next_step_handler(message, translator)
def translator(message):
    user_id = message.from_user.id
    text = message.text
    if text[0].lower() in ru_letters:
        translator = Translator(from_lang="russian", to_lang="uzbek")
        translation = translator.translate(message.text)
        print(translation)
        bot.send_message(user_id, translation)
    # translator = Translator(from_lang="russian", to_lang="uzbek")
    elif text[0].lower() in uz_letters:
        translator = Translator(from_lang="uzbek", to_lang="russian")
        translation = translator.translate(message.text)
        print(translation)
        bot.send_message(user_id, translation)



bot.infinity_polling()

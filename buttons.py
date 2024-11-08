from telebot import types

def lang():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("RU")
    button1 = types.KeyboardButton("UZ")
    kb.add(button)
    kb.add(button1)
    return kb



def phone_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Поделиться контактом!", request_contact=True)
    button1 = types.KeyboardButton("Aloqani baham ko'ring", request_contact=True)
    kb.add(button)
    kb.add(button1)
    return kb
def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Поделиться локацией!", request_location=True)
    button1 = types.KeyboardButton("Joylashuvni ulashish!", request_location=True)
    kb.add(button)
    kb.add(button1)
    return kb


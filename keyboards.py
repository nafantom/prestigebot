from telebot.types import *

def generate_registration():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Записаться на платный мок')
    btn_info = KeyboardButton(text='О насℹ')
    markup.add(btn, btn_info)
    return markup

def generate_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Отправить контакт', request_contact=True)
    markup.add(btn)
    return markup

def generate_time():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton(text='9:30')
    btn2 = KeyboardButton(text='14:30')
    markup.add(btn1, btn2)
    return markup


def generate_yes_no():
    markup = InlineKeyboardMarkup()
    btn_yes = InlineKeyboardButton(text='Подтвердить ✅', callback_data='yes')
    btn_no = InlineKeyboardButton(text='Отменить❌', callback_data='no')
    markup.add(btn_yes, btn_no)
    return markup


from telebot import *
from telebot.types import *
from configs import *
from database import *
from keyboards import *


bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Приветствуем вас в боте нашего учебного центра😊.',
                     reply_markup=generate_registration())

@bot.message_handler(func=lambda message: 'Информация о центре' == message.text)
def info(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'''Prestige IELTS Academy находится по адресу: Чиланзарский район, квартал Ц, 48.
Ориентир: метро «Мирзо Улугбек», театр Оперетты.
Рабочее время: с понедельника по субботу с 9:00 до 20.00.

Контакты:

+998-95-227-99-00

+998-97-725-01-99''')
    bot.send_message(chat_id, 'https://maps.app.goo.gl/ENzBnai3BHFMo7PH7')


@bot.message_handler(func=lambda message: 'Информация о MOCK-Test' == message.text)
def mock(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''• Цена МОСК-Test - 150 000 сум;
• MOCK-Test включает в себя все аспекты IELTS.
• В первый день проводятся - Reading, Listening, Writing и во второй день - Speaking;
• Результаты MOCK-Test Вы получить на второй день после сдачи Speaking!

Для регистрации нажмите на кнопку «Зарегистрироваться на тест»👇''', reply_markup=generate_mock())


@bot.message_handler(func=lambda message: 'Зарегистрироваться на тест' == message.text)
def ask_full_name(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Напишите своё имя и фамилию: ', reply_markup=None)
    bot.register_next_step_handler(msg, ask_phone_number)


def ask_phone_number(message: Message):
    global user_data
    chat_id = message.chat.id
    full_name = message.text
    user_data['full_name'] = full_name
    msg = bot.send_message(chat_id, f'Отправьте ваш контакт: ', reply_markup=generate_contact())
    bot.register_next_step_handler(msg, ask_date)
    bot.send_message(chat_id, 'Нажмите на кнопку для отправки контакта')

def ask_date(message: Message):
    global user_data
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    user_data['phone_number'] = phone_number
    msg = bot.send_message(chat_id, f'Напишите дату на которую вы хотите записаться:')
    bot.register_next_step_handler(msg, ask_time)

def ask_time(message: Message):
    global user_data
    chat_id = message.chat.id
    date = message.text
    user_data['date'] = date
    msg = bot.send_message(chat_id, f'Выберите время на кторое вы хотите записаться: ', reply_markup=generate_time())
    bot.register_next_step_handler(msg, end_register)

def end_register(message: Message):
    global user_data
    chat_id = message.chat.id
    time = message.text
    user_data['time'] = time
    bot.send_message(chat_id, f'''
Имя и Фамилия: {user_data['full_name']}    
Номер телефона: {user_data['phone_number']}
Дата: {user_data['date']}
Время: {user_data['time']}
''', reply_markup=generate_yes_no())

@bot.callback_query_handler(func=lambda call: 'yes' == call.data)
def submit_registration(call: CallbackQuery):
    global users
    chat_id = call.message.chat.id

    database = sqlite3.connect('users.db')
    cursor = database.cursor()

    cursor.execute('''
INSERT INTO users(telegram_id, full_name, phone_number, date, time) 
VALUES (?, ?, ?, ?, ?) 
    ''', (chat_id, user_data['full_name'], user_data['phone_number'], user_data['date'], user_data['time']))

    bot.send_message(chat_id, f'Вы успешно записались на наш мок тест!😁'
                              f'Ваши данные: \n'
                              f'Имя:\t {user_data['full_name']}\n'
                              f'Номер телефона:\t {user_data['phone_number']}\n'
                              f'Дата мок теста:\t {user_data['date']}\n'
                              f'Время:\t {user_data['time']}\n'
                              f'Произвести оплату в 150 тысч сум за мок тест вы сможете у нас в офисе в день теста.\n'
                              f'Просим вас прийти за 20 минут до начала теста, что бы успеть вовремя зайти на него.\n'
                              f'Good Luck😉🍀'
                              )

    bot.send_message(GROUP_ID, f'Платный мок:\n'
                               f'Имя:\t {user_data['full_name']}\n'
                              f'Номер телефона:\t {user_data['phone_number']}\n'
                              f'Дата мок теста:\t {user_data['date']}\n'
                              f'Время:\t {user_data['time']}')
    database.commit()
    database.close()
    user_data.clear()


@bot.callback_query_handler(func=lambda call: 'no' == call.data)
def unsubmit_registration(call: CallbackQuery):
    chat_id = call.message.chat.id
    msg = bot.send_message(chat_id, f'Вы успешно отменили запись!')
    bot.register_next_step_handler(msg, reply_markup=generate_registration())



bot.polling(none_stop=True)
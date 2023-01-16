import telebot
from config import bot_token, admin_id, group_id
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time
import pytz

bot = telebot.TeleBot(f'{bot_token}')

# Подсоединение к Google Таблицам
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

#Открытие таблицы
global worksheet
sheet = client.open("TestDatabase")
worksheet = sheet.sheet1

# Старт бот
@bot.message_handler(commands=['start_bot'])
def start_bot(message):
    if message.from_user.id == 775928781:
        bot.send_message(message.chat.id, f'Бот був переведений в робочий стан')
        print('Bot run: OK')
        return process_day()


@bot.message_handler(commands=['start'])
def start(message):

#Если пользователь не является админом
    if message.from_user.id != 775928781:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        question = types.KeyboardButton('Залишити відгук чи запитання✉️')
        #actual = types.KeyboardButton('Відключення сьогодні⚡️(В розробці)')
        markup.add(question)
        bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} \n мене створив https://t.me/dmitriy_zaytsev')
        bot.send_message(message.chat.id, f'Якщо ти хочеш допомогти розробнику цього бота\nТо будемо дуже вдячні за кожну донат гривню😄\n\nНомер картки:\nMonobank: 5375 4141 1352 3004\nPrivatBank: 4149 6293 5699 0291\nХорошого тобі дня☺️', reply_markup=markup,parse_mode='html')

#Если пользователь является админом
    if message.from_user.id == 775928781:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        announcement = types.KeyboardButton('Оголошення')
        price = types.KeyboardButton('Актуальний графік')
        markup.add(announcement, price)
        bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} \nготов до роботи?', reply_markup=markup,parse_mode='html')

#Процесс определения текущей даты
def process_day():
    #Определение текущей даты по Киеву
    global date_day
    tz_kiev = pytz.timezone("Europe/Kiev" )
    date_day = datetime.datetime.now(tz_kiev).strftime("%d")

    #Поиск даты в таблице
    global result_date
    find_date = worksheet.find(date_day)
    result_date = find_date.col
    time.sleep(10)
    return process_hour()

#Процесс определения текущего времени
def process_hour():
    tz_kiev = pytz.timezone("Europe/Kiev")
    dateSTR = datetime.datetime.now(tz_kiev).strftime("%H:%M")
    print(f'Date: {date_day}          Time: {dateSTR}          Table Row: {result_date}          BOT status: OK')

    #Процесс сравнивание
    if dateSTR == ("00:20"):
        val = worksheet.cell(4, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 00:30 - 03:00')
        time.sleep(480)

    elif dateSTR == ("00:30"):
        val = worksheet.cell(4, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        time.sleep(6600)

    if dateSTR == ("02:50"):
        val = worksheet.cell(5, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 03:00 - 05:30')
        time.sleep(480)

    elif dateSTR == ("03:00"):
        val = worksheet.cell(5, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        time.sleep(6600)

    if dateSTR == ("05:20"):
        val = worksheet.cell(6, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 05:30 - 08:00')
        time.sleep(480)
    elif dateSTR == ("05:30"):
        val = worksheet.cell(6, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 05:30 - 08:00')
        time.sleep(6600)

    if dateSTR == ("07:50"):
        val = worksheet.cell(7, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 08:00 - 10:00')
        time.sleep(480)
    elif dateSTR == ("08:00"):
        val = worksheet.cell(7, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 08:00 - 10:00')
        time.sleep(6600)

    if dateSTR == ("09:50"):
        val = worksheet.cell(8, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 10:00 - 12:00')
        time.sleep(480)
    elif dateSTR == ("10:00"):
        val = worksheet.cell(8, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 10:00 - 12:00')
        time.sleep(6600)

    if dateSTR == ("11:50"):
        val = worksheet.cell(9, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 12:00 - 14:00')
        time.sleep(480)
    elif dateSTR == ("12:00"):
        val = worksheet.cell(9, result_date).value
        print(val)
        bot.send_message(-1001841821249, f'Зараз можливе відключено світла\n{val}\nНа період 12:00 - 14:00')
        time.sleep(6600)

    if dateSTR == ("13:50"):
        val = worksheet.cell(10, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 14:00 - 16:00')
        time.sleep(480)
    elif dateSTR == ("14:00"):
        val = worksheet.cell(10, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 14:00 - 16:00')
        time.sleep(6600)

    if dateSTR == ("15:50"):
        val = worksheet.cell(11, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 16:00 - 18:00')
        time.sleep(480)
    elif dateSTR == ("16:00"):
        val = worksheet.cell(11, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 16:00 - 18:00')
        time.sleep(6600)

    if dateSTR == ("17:50"):
        val = worksheet.cell(12, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 18:00 - 20:00')
        time.sleep(480)
    elif dateSTR == ("18:00"):
        val = worksheet.cell(12, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 18:00 - 20:00')
        time.sleep(6600)

    if dateSTR == ("19:50"):
        val = worksheet.cell(13, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 20:00 - 22:00')
        time.sleep(480)
    elif dateSTR == ("20:00"):
        val = worksheet.cell(13, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 20:00 - 22:00')
        time.sleep(6600)

    if dateSTR == ("21:50"):
        val = worksheet.cell(14, result_date).value
        print(val)
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 22:00 - 00:30')
        time.sleep(480)
    elif dateSTR == ("22:00"):
        val = worksheet.cell(14, result_date).value
        print(val)
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 18:00 - 20:00')
        time.sleep(6600)
    time.sleep(10)
    return process_day()

# Проверка сообщения пользователя
@bot.message_handler(content_types=['text'])
#Пользовательские функции
#Задать вопрос
def question(message):
    if message.text == "Залишити відгук чи запитання✉️":
        msg = bot.send_message(message.chat.id, '<b>Введіть ваше повідомлення</b>', parse_mode='html')
        bot.register_next_step_handler(msg, question_next_step)

#Получение графика Q4-Q14
    #if message.text == "Відключення сьогодні⚡️":
        #print('123')
        #graf =  worksheet.col_values(6)
        #bot.send_message(message.chat.id, '<b>Графік відключень на сьогодні</b>', parse_mode='html')
        #bot.send_message(message.chat.id, f'<b>{graf}</b>', parse_mode='html')

    if message.from_user.id == 775928781:
        if message.text == "Оголошення":
            msg = bot.send_message(message.chat.id, '<b>Введіть ваше повідомлення</b>', parse_mode='html')
            bot.register_next_step_handler(msg, announcement_next_step)

#Отправка вопроса
def question_next_step(message):
    message_question = message.text
    bot.send_message(admin_id, f'Вопрос: {message_question} \n\n\nЗадал:  https://t.me/{message.from_user.username}')

#Отправка обьявления
def announcement_next_step(message):
    message_announcement = message.text
    bot.send_message(group_id, {message_announcement})

bot.polling(none_stop=True)
import telebot
from telebot import types
import mysql.connector
from allfiles.config import bot_token, admin_id, group_id
from allfiles.table import process_day
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time
import pytz
bot = telebot.TeleBot(bot_token)

#Данные для подключение к БД
db = mysql.connector.connect(
    host="localhost",
    user="BD USER",
    password="BD PASSWORD",
    port="3306",
    database="DB"
)
cursor = db.cursor()

# Подсоединение к Google Таблицам
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

#Открытие таблицы
global worksheet
sheet = client.open("SHEET NAME")
worksheet = sheet.sheet1

#Активация функций расчёта и разсылки бота
@bot.message_handler(commands=['start_bot'])
def start_bot(message):
    if message.from_user.id == ADMIN ID:
        bot.send_message(message.chat.id, f'Бот був переведений в робочий стан')
        print('Bot run: OK')
        return process_day()

    process_day()

#Стартовое меню пользователя
@bot.message_handler(commands=['start'])
def start(message):
    #Проверка и добавление пользователя в бд
    try:
        global us_id
        global user_id
        user_name = message.from_user.first_name
        user_login = message.from_user.username
        user_id = message.from_user.id
        cursor.execute(f"SELECT id FROM alarm_table WHERE id = {user_id}")
        us_id = cursor.fetchone()

        #Запись пользователя в БД
        if us_id is None:
            sql = "INSERT INTO alarm_table (id, login, name) VALUES (%s, %s, %s)"
            val = (user_id, user_login, user_name)
            cursor.execute(sql, val)
            cursor.execute(f"UPDATE alarm_table SET spam = 'yes' WHERE id = {user_id}")
            db.commit()

            # Если пользователь не является админом
            if message.from_user.id != ADMIN ID:
                telebot.types.ReplyKeyboardRemove()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                question = types.KeyboardButton('Залишити відгук чи запитання✉️')
                premium = types.KeyboardButton('Меню ⚡️')
                probot = types.KeyboardButton('Про бота')
                markup.add(question, premium, probot)
                bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}',reply_markup=markup)

        else:
            # Если пользователь не является админом
            if message.from_user.id != ADMIN ID:
                telebot.types.ReplyKeyboardRemove()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                question = types.KeyboardButton('Залишити відгук чи запитання✉️')
                premium = types.KeyboardButton('Меню ⚡️')
                probot = types.KeyboardButton('Про бота')
                markup.add(question, premium, probot)
                bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}',reply_markup=markup)

             # Если пользователь является админом
            if message.from_user.id == ADMIN ID:
                telebot.types.ReplyKeyboardRemove()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                announcement = types.KeyboardButton('Оголошення')
                actual = types.KeyboardButton('Актуальний графік відключень')
                markup.add(announcement, actual)
                bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}',reply_markup=markup, parse_mode='html')

    except:
        bot.send_message(message.chat.id, f'🚫 | Помилка')

# Проверка сообщения пользователя
@bot.message_handler(content_types=['text'])
#Пользовательские функции
def menu(message):
    #Главное меню пользователя
    if message.text == "Меню ⚡️":
        user_id = message.from_user.id
        telebot.types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        cher = types.KeyboardButton('Змінити чергу')
        misto = types.KeyboardButton('Змінити місто')
        actual_graf_off = types.KeyboardButton('Актуальний графік відключень')
        active_spam = types.KeyboardButton('Переключити розсилання')
        back = types.KeyboardButton('Назад')
        markup.add(actual_graf_off, cher, misto, active_spam, back)
        bot.send_message(message.chat.id, f'Ви перейшли до меню', reply_markup=markup, parse_mode='html')

    #Кнопка возврата в прошлое меню    
    if message.text == "Назад":
        telebot.types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        question = types.KeyboardButton('Залишити відгук чи запитання✉️')
        premium = types.KeyboardButton('Меню ⚡️')
        probot = types.KeyboardButton('Про бота')
        markup.add(question, premium, probot)
        bot.send_message(message.chat.id, f'Чим можу допомогти?', reply_markup=markup, parse_mode='html')



#Функция выбора очереди
    if message.text == "Змінити чергу":
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup()
        onecherga = types.InlineKeyboardButton('1 черга', callback_data="onecher")
        twocherga = types.InlineKeyboardButton('2 черга', callback_data="twocher")
        fricherga = types.InlineKeyboardButton('3 черга', callback_data="fricher")
        markup.add(onecherga, twocherga, fricherga)
        bot.send_message(message.chat.id, 'Оберіть вашу чергу:', reply_markup=markup)
#Функция выбора города
    if message.text == "Змінити місто":
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup()
        dykmisto = types.InlineKeyboardButton('Диканська дільниця', callback_data="mistodik")
        zinkmisto = types.InlineKeyboardButton('Зіньківська дільниця', callback_data="mistozik")
        markup.add(dykmisto, zinkmisto)
        bot.send_message(message.chat.id, 'Виберіть до якої дільниці ви підключені:', reply_markup=markup)

#Функция получения графика на сегодня
    if message.text == "Актуальний графік відключень":
        user_id = message.from_user.id
        tz_kiev = pytz.timezone("Europe/Kiev" )
        day = datetime.datetime.now(tz_kiev).strftime("%d")
        find_date = worksheet.find(day)
        result_date = find_date.col
        result_graf_time = worksheet.col_values(1)
        result_graf_date = worksheet.col_values(result_date)
        bot.send_message(message.chat.id, f'Графік на {day}  день місяця\nЧас: *{result_graf_time[3]} || {result_graf_date[3]}* \nЧас: *{result_graf_time[4]} || {result_graf_date[4]}* \nЧас: *{result_graf_time[5]} || {result_graf_date[5]}* \nЧас: *{result_graf_time[6]} || {result_graf_date[6]}* \nЧас: *{result_graf_time[7]} || {result_graf_date[7]}* \nЧас: *{result_graf_time[8]} || {result_graf_date[8]}* \nЧас: *{result_graf_time[9]} || {result_graf_date[9]}* \nЧас: *{result_graf_time[10]} || {result_graf_date[10]}* \nЧас: *{result_graf_time[11]} || {result_graf_date[11]}* \nЧас: *{result_graf_time[12]} || {result_graf_date[12]}* \nЧас: *{result_graf_time[13]} || {result_graf_date[13]}*', parse_mode="Markdown")

#Функция обьявлений в канал
    if message.from_user.id == ADMIN ID:
        if message.text == "Оголошення":
            msg = bot.send_message(message.chat.id, '<b>Введіть ваше повідомлення</b>', parse_mode='html')
            bot.register_next_step_handler(msg, announcement_next_step)

#Фукнция включения\отключения получения уведомлений пользователем от бота
    if message.text == "Переключити розсилання":
        markup = types.InlineKeyboardMarkup()
        on = types.InlineKeyboardButton('Вкл розсилання', callback_data="on_spam")
        off = types.InlineKeyboardButton('Викл розсилання', callback_data="off_spam")
        markup.add(on, off)
        bot.send_message(message.chat.id, 'Переключення розсилання:', reply_markup=markup)

#Задать вопрос администрации
    if message.text == "Залишити відгук чи запитання✉️":
        msg = bot.send_message(message.chat.id, '<b>Введіть ваше повідомлення</b>', parse_mode='html')
        bot.register_next_step_handler(msg, question_next_step)

#Отправка вопроса
def question_next_step(message):
    message_question = message.text
    bot.send_message(admin_id, f'Вопрос: {message_question} \n\n\nЗадав:  https://t.me/{message.from_user.username}')

#Отправка обьявления
def announcement_next_step(message):
    message_announcement = message.text
    bot.send_message(group_id, {message_announcement})

#Обработчик нажатий кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    #Выбор очереди
    #Первая очередь
    if call.data == 'onecher':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали 1 чергу')
        sql = f"UPDATE alarm_table SET cherga = '1' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    #Вторая очередь
    if call.data == 'twocher':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали 2 чергу')
        sql = f"UPDATE alarm_table SET cherga = '2' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    #Третья очередь
    if call.data == 'fricher':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали 3 чергу')
        sql = f"UPDATE alarm_table SET cherga = '3' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    #Выбор города
    #Город Диканька
    if call.data == 'mistodik':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали Диканська дільниця')
        sql = f"UPDATE alarm_table SET misto = 'Диканька' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    #Город Зіньків
    if call.data == 'mistozik':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали Зіньківська дільниця')
        sql = f"UPDATE alarm_table SET misto = 'Зіньків' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    #Выбор режима разсылки
    #Вкл разсылку
    if call.data == 'on_spam':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви  увімкнули розсилання')
        sql = f"UPDATE alarm_table SET spam = 'yes' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    #Выкл разсылку
    if call.data == 'off_spam':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви вимкнули розсилання')
        sql = f"UPDATE alarm_table SET spam = 'no' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

bot.polling(none_stop=True)
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

db = mysql.connector.connect(
    host="localhost",
    user="alarmbot",
    password="rabbit2005",
    port="3306",
    database="alarm"
)

cursor = db.cursor()

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
            db.commit()

            # Если пользователь не является админом
            if message.from_user.id != 775928781:
                telebot.types.ReplyKeyboardRemove()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                question = types.KeyboardButton('Залишити відгук чи запитання✉️')
                premium = types.KeyboardButton('Преміум ⚡️')
                probot = types.KeyboardButton('Про бота')
                markup.add(question, premium, probot)
                bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} \n Бот знаходиться в розробці',reply_markup=markup)

        else:
            # Если пользователь не является админом
            if message.from_user.id != 775928781:
                telebot.types.ReplyKeyboardRemove()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                question = types.KeyboardButton('Залишити відгук чи запитання✉️')
                premium = types.KeyboardButton('Преміум ⚡️')
                probot = types.KeyboardButton('Про бота')
                markup.add(question, premium, probot)
                bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} \n Бот знаходиться в розробці',reply_markup=markup)

             # Если пользователь является админом
            if message.from_user.id == 775928781:
                telebot.types.ReplyKeyboardRemove()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                announcement = types.KeyboardButton('Оголошення')
                actual = types.KeyboardButton('Актуальний графік відключень')
                markup.add(announcement, actual)
                bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} \nготов до роботи?',reply_markup=markup, parse_mode='html')

    except:
        bot.send_message(message.chat.id, f'🚫 | Помилка')

# Проверка сообщения пользователя
@bot.message_handler(content_types=['text'])
#Пользовательские функции
#Премиум функции
#Определение пользователя как премиум
def menu(message):
    if message.text == "Преміум ⚡️":
        global premium_yes
        global premium_result
        premium_yes = [('yes',)]
        user_id = message.from_user.id
        select_query = """SELECT premium FROM alarm_table WHERE id = %s"""
        cursor.execute(select_query, (user_id,))
        premium_result = cursor.fetchall()

        if premium_yes == premium_result:
            telebot.types.ReplyKeyboardRemove()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            cher = types.KeyboardButton('Змінити чергу')
            misto = types.KeyboardButton('Змінити місто')
            #data_off = types.KeyboardButton('Данні відключень')
            actual_graf_off = types.KeyboardButton('Актуальний графік відключень')
            markup.add(actual_graf_off, cher, misto)
            bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}! \nЧим можу допомогти?', reply_markup=markup, parse_mode='html')

        if premium_yes != premium_result:
            bot.send_message(message.chat.id, 'В розробці\nВи зможете придбати потім')

#Функция выбора черги
    if message.text == "Змінити чергу":
        markup = types.InlineKeyboardMarkup()
        onecherga = types.InlineKeyboardButton('1 черга', callback_data="onecher")
        twocherga = types.InlineKeyboardButton('2 черга', callback_data="twocher")
        fricherga = types.InlineKeyboardButton('3 черга', callback_data="fricher")
        markup.add(onecherga, twocherga, fricherga)
        bot.send_message(message.chat.id, 'Оберіть вашу чергу:', reply_markup=markup)

    if message.text == "Змінити місто":
        markup = types.InlineKeyboardMarkup()
        dykmisto = types.InlineKeyboardButton('Диканська дільниця', callback_data="mistodik")
        zinkmisto = types.InlineKeyboardButton('Зіньківська дільниця', callback_data="mistozik")
        markup.add(dykmisto, zinkmisto)
        bot.send_message(message.chat.id, 'Виберіть до якої дільниці ви підключені:', reply_markup=markup)

#Функция получения графика на сегодня с повторной проверкой премиума во избежание вылетов
    if message.text == "Актуальний графік відключень":
        premium_yes = [('yes',)]
        user_id = message.from_user.id
        select_query = """SELECT premium FROM alarm_table WHERE id = %s"""
        cursor.execute(select_query, (user_id,))
        premium_result = cursor.fetchall()
        if premium_yes == premium_result:
            tz_kiev = pytz.timezone("Europe/Kiev" )
            day = datetime.datetime.now(tz_kiev).strftime("%d")
            find_date = worksheet.find(day)
            result_date = find_date.col
            result_graf_time = worksheet.col_values(1)
            result_graf_date = worksheet.col_values(result_date)

            bot.send_message(message.chat.id, f'Графік на {day}  день місяця\nЧас: *{result_graf_time[3]} || {result_graf_date[3]}* \nЧас: *{result_graf_time[4]} || {result_graf_date[4]}* \nЧас: *{result_graf_time[5]} || {result_graf_date[5]}* \nЧас: *{result_graf_time[6]} || {result_graf_date[6]}* \nЧас: *{result_graf_time[7]} || {result_graf_date[7]}* \nЧас: *{result_graf_time[8]} || {result_graf_date[8]}* \nЧас: *{result_graf_time[9]} || {result_graf_date[9]}* \nЧас: *{result_graf_time[10]} || {result_graf_date[10]}* \nЧас: *{result_graf_time[11]} || {result_graf_date[11]}* \nЧас: *{result_graf_time[12]} || {result_graf_date[12]}* \nЧас: *{result_graf_time[13]} || {result_graf_date[13]}*', parse_mode="Markdown")
        elif premium_yes != premium_result:
            bot.send_message(message.chat.id, 'Вибачте, ця функція доступна лише з підпискою "Преміум"')

    if message.from_user.id == 775928781:
        if message.text == "Оголошення":
            msg = bot.send_message(message.chat.id, '<b>Введіть ваше повідомлення</b>', parse_mode='html')
            bot.register_next_step_handler(msg, announcement_next_step)

        #Функция разсылки
    #if message.text == "test":
    #    loh(message)
        #cursor.execute(f"SELECT id FROM alarm_table WHERE spam = 'yes'")
        #all_id = cursor.fetchall()
        #msg = 'suka'
        #for x in all_id:
        #    bot.send_message(x[0], str(msg))
        #    print(x)
        #db.commit()

        #tz_kiev = pytz.timezone("Europe/Kiev" )
        #date_hour = datetime.datetime.now(tz_kiev).strftime("%H:%M")
        #date_hour = '00:30 - 03:00'
        #find_hour = worksheet.find(date_hour)
        #print(find_hour)


        #global date_day
        #tz_kiev = pytz.timezone("Europe/Kiev" )
        #dateSTR = datetime.datetime.now(tz_kiev).strftime("%H:%M")

        #Поиск даты в таблице
        #global result_date
        #find_date = worksheet.find(date_day)
        #result_date = find_date.col

        #if dateSTR == ("00:20"):
        #val = worksheet.cell(dateSTR, result_date).value
        #print(val)
        #bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 00:30 - 03:00')

        #tz_kie = pytz.timezone("Europe/Kiev" )
        #date_da = datetime.datetime.now(tz_kie).strftime("%d")
        #find_dat = worksheet.find(date_da)
        #result_dat = find_dat.col
        #val = worksheet.cell(4, result_dat).value
        #if val == ('1 (та 3) черга'):
        #    print ('test1')
        #if val == ('2 (та 1) черга'):
        #    print ('test1')
        #if val == ('3 (та2) черга'):
        #    print ('test1')
        #print(val)



        #if premium_yes == premium_result:
        #    telebot.types.ReplyKeyboardRemove()
        #   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        #    cher = types.KeyboardButton('Змінити чергу')
        #    misto = types.KeyboardButton('Змінити місто')
        #    #data_off = types.KeyboardButton('Данні відключень')
        #    actual_graf_off = types.KeyboardButton('Актуальний графік відключень')
        #    markup.add(actual_graf_off, cher, misto)
        #    bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}! \nЧим можу допомогти?', reply_markup=markup, parse_mode='html')


        #if message.text == "Розсылка":
        #    cursor.execute(f"SELECT id FROM alarm_table")
        #    us_id = cursor.fetchall()
        #    print(us_id)
        #    msg = 'Тест'
        #    for x in us_id:
         #       bot.send_message(x[0], str(msg))



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

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    #Очередь
    if call.data == 'onecher':
        user_id = call.message.from_user.id
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали 1 чергу')
        sql = f"UPDATE alarm_table SET cherga = '1' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    if call.data == 'twocher':
        user_id = call.message.from_user.id
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали 2 чергу')
        sql = f"UPDATE alarm_table SET cherga = '2' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    if call.data == 'fricher':
        user_id = call.message.from_user.id
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали 3 чергу')
        sql = f"UPDATE alarm_table SET cherga = '3' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    #Город
    if call.data == 'mistodik':
        user_id = call.message.from_user.id
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали Диканська дільниця')
        sql = f"UPDATE alarm_table SET misto = 'Диканька' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

    if call.data == 'mistozik':
        user_id = call.message.from_user.id
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 'Ви обрали Зіньківська дільниця')
        sql = f"UPDATE alarm_table SET misto = 'Зіньків' WHERE id = {user_id}"
        cursor.execute(sql)
        db.commit()

bot.polling(none_stop=True)
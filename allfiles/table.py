import telebot
import mysql.connector
from allfiles.config import bot_token, admin_id, group_id
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time
import pytz
bot = telebot.TeleBot(bot_token)

#Данные подключения к БД
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
    cursor.execute(f"SELECT id FROM alarm_table WHERE id = 775928781")
    result = cursor.fetchone()
    print(f'Date: {date_day}          Time: {dateSTR}          Table Row: {result_date}          BOT status: OK')
    print(f'Mysql STATUS {result}')

    #Функция процесса сравнивания времени относительно заданного и сравнивания с 2 данными пользователя из БД
    #И разсылка исходя из полученых данных
    if dateSTR == ("00:20"):
        val = worksheet.cell(4, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 00:30 - 03:00')

        time.sleep(480)

    elif dateSTR == ("00:30"):
        val = worksheet.cell(4, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 00:30 - 03:00')
        time.sleep(6600)

    if dateSTR == ("02:50"):
        val = worksheet.cell(5, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        time.sleep(480)

    elif dateSTR == ("03:00"):
        val = worksheet.cell(5, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 03:00 - 05:30')
        time.sleep(6600)

    if dateSTR == ("05:20"):
        val = worksheet.cell(6, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 05:30 - 08:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 05:30 - 08:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 05:30 - 08:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 05:30 - 08:00')
        time.sleep(480)
    elif dateSTR == ("05:30"):
        val = worksheet.cell(6, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 05:30 - 08:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 05:30 - 08:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 05:30 - 08:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 05:30 - 08:00')
        time.sleep(6600)

    if dateSTR == ("07:50"):
        val = worksheet.cell(7, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 08:00 - 10:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 08:00 - 10:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 08:00 - 10:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 08:00 - 10:00')
        time.sleep(480)

    elif dateSTR == ("08:00"):
        val = worksheet.cell(7, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 08:00 - 10:00')
        tz_kiev = pytz.timezone("Europe/Kiev" )
        day = datetime.datetime.now(tz_kiev).strftime("%d")
        find_date_group = worksheet.find(day)
        result_date_group = find_date_group.col
        result_graf_time = worksheet.col_values(1)
        result_graf_date = worksheet.col_values(result_date_group)
        bot.send_message(group_id, f'Доброго ранку, на годиннику *08:00* і графік на *{day}* день місяця  слідуючий\nЧас: *{result_graf_time[3]} || {result_graf_date[3]}* \nЧас: *{result_graf_time[4]} || {result_graf_date[4]}* \nЧас: *{result_graf_time[5]} || {result_graf_date[5]}* \nЧас: *{result_graf_time[6]} || {result_graf_date[6]}* \nЧас: *{result_graf_time[7]} || {result_graf_date[7]}* \nЧас: *{result_graf_time[8]} || {result_graf_date[8]}* \nЧас: *{result_graf_time[9]} || {result_graf_date[9]}* \nЧас: *{result_graf_time[10]} || {result_graf_date[10]}* \nЧас: *{result_graf_time[11]} || {result_graf_date[11]}* \nЧас: *{result_graf_time[12]} || {result_graf_date[12]}* \nЧас: *{result_graf_time[13]} || {result_graf_date[13]}*', parse_mode="Markdown")
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 08:00 - 10:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 08:00 - 10:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 08:00 - 10:00')
        time.sleep(6600)

    if dateSTR == ("09:50"):
        val = worksheet.cell(8, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 10:00 - 12:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 10:00 - 12:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 10:00 - 12:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 10:00 - 12:00')
        time.sleep(480)

    elif dateSTR == ("10:00"):
        val = worksheet.cell(8, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 10:00 - 12:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 10:00 - 12:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 10:00 - 12:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 10:00 - 12:00')
        time.sleep(6600)

    if dateSTR == ("11:50"):
        val = worksheet.cell(9, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 12:00 - 14:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 12:00 - 14:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 12:00 - 14:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 12:00 - 14:00')
        time.sleep(480)

    elif dateSTR == ("12:00"):
        val = worksheet.cell(9, result_date).value
        bot.send_message(-1001841821249, f'Зараз можливе відключено світла\n{val}\nНа період 12:00 - 14:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 12:00 - 14:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 12:00 - 14:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 12:00 - 14:00')
        time.sleep(6600)

    if dateSTR == ("13:50"):
        val = worksheet.cell(10, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 14:00 - 16:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 14:00 - 16:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 14:00 - 16:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 14:00 - 16:00')
        time.sleep(480)

    elif dateSTR == ("14:00"):
        val = worksheet.cell(10, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 14:00 - 16:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 14:00 - 16:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 14:00 - 16:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 14:00 - 16:00')
        time.sleep(6600)

    if dateSTR == ("15:50"):
        val = worksheet.cell(11, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 16:00 - 18:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 16:00 - 18:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 16:00 - 18:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 16:00 - 18:00')
        time.sleep(480)

    elif dateSTR == ("16:00"):
        val = worksheet.cell(11, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 16:00 - 18:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 16:00 - 18:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 16:00 - 18:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 16:00 - 18:00')
        time.sleep(6600)

    if dateSTR == ("17:50"):
        val = worksheet.cell(12, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 18:00 - 20:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 18:00 - 20:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 18:00 - 20:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 18:00 - 20:00')
        time.sleep(480)

    elif dateSTR == ("18:00"):
        val = worksheet.cell(12, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 18:00 - 20:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 18:00 - 20:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 18:00 - 20:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 18:00 - 20:00')
        time.sleep(6600)

    if dateSTR == ("19:50"):
        val = worksheet.cell(13, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 20:00 - 22:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 20:00 - 22:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 20:00 - 22:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 20:00 - 22:00')
        time.sleep(480)

    elif dateSTR == ("20:00"):
        val = worksheet.cell(13, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 20:00 - 22:00')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 20:00 - 22:00')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 20:00 - 22:00')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 20:00 - 22:00')
        time.sleep(6600)

    if dateSTR == ("21:50"):
        val = worksheet.cell(14, result_date).value
        bot.send_message(group_id, f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 22:00 - 00:30')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 22:00 - 00:30')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 22:00 - 00:30')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Через 10 хвилин можливе відключення світла\n{val}\nНа період 22:00 - 00:30')
        time.sleep(480)

    elif dateSTR == ("22:00"):
        val = worksheet.cell(14, result_date).value
        bot.send_message(group_id, f'Зараз можливе відключено світла\n{val}\nНа період 22:00 - 00:30')
        if val == ('1 (та 3) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '1' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 22:00 - 00:30')
        if val == ('2 (та 1) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '2' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 22:00 - 00:30')
        if val == ('3 (та2) черга'):
            db.commit()
            cursor.execute(f"SELECT id FROM alarm_table WHERE cherga = '3' AND spam = 'yes'")
            all_id = cursor.fetchall()
            for x in all_id:
                bot.send_message(x[0], f'Зараз можливе відключено світла\n{val}\nНа період 22:00 - 00:30')
        time.sleep(6600)


    time.sleep(10)
    return process_day()


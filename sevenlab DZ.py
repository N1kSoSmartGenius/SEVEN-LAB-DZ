import telebot
from telebot import types
import psycopg2
import datetime

today_day = (datetime.datetime.today().weekday())

token = "6360649611:AAG2ZXn6WdgHgeVrJYkw2n6xyypl_hIrhyc"
bot = telebot.TeleBot(token)
conn = psycopg2.connect(database='tg_bot',
                        user = 'postgres',
                        password = '5591',
                        host = 'localhost',
                        port = '5432',
)

cursor = conn.cursor()
week = 11
if today_day == 6:
    week += 1




@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу","/help")
    bot.send_message(message.chat.id, f'Здравствуйте! Хотите узнать свежую информацию о МТУСИ? Если вы не хотите узнать свежую информацию но хотите узнать что умеет этот бот, то смело жмите кнопку /help', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    global keyboard_menu
    keyboard_menu = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,one_time_keyboard=False)
    button_exit = telebot.types.KeyboardButton('Выход в главное меню')
    button_Monday = telebot.types.KeyboardButton('Понедельник')
    button_Tuesday = telebot.types.KeyboardButton('Вторник')
    button_Wednesday = telebot.types.KeyboardButton('Среда')
    button_Thursday = telebot.types.KeyboardButton('Четверг')
    button_Friday = telebot.types.KeyboardButton('Пятница')
    button_Saturday = telebot.types.KeyboardButton('Суббота')
    button_website = telebot.types.KeyboardButton('Сайт нашего вуза')
    button_week = telebot.types.KeyboardButton('Текущая неделя')
    button_timetable_to_this_week = telebot.types.KeyboardButton('Расписание на текущую неделю')
    button_timetable_to_next_week = telebot.types.KeyboardButton('Расписание на следующую неделю')
    keyboard_menu.add(button_exit, button_week, button_website, button_Monday, button_Tuesday, button_Wednesday, button_Thursday, button_Friday, button_Saturday,button_timetable_to_this_week, button_timetable_to_next_week)
    bot.send_message(message.chat.id, 'Я бот, который прекрасно знает расписание вашей группы (БИН2308). Вы можете получить как текущее расписание, так и на следующую неделю. Вы также можете получить расписание на 1 день, просто выбрав 1 из дней текущей недели. Сейчас на экране вы видите все возможные команды',reply_markup=keyboard_menu)

@bot.message_handler(commands=['exit'])
def exit(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу","/help")
    bot.send_message(message.chat.id,'О, это снова вы? Я рад что вы вернулись. Хотите ещё узнать информацию о МТУСИ? Если нет, то смело жмите кнопку /help и получите всю информацию обо мне!',reply_markup=keyboard)
@bot.message_handler(commands=['week'])
def give_week(message):
    if week % 2 == 0:
        bot.send_message(message.chat.id, f'Сейчас идёт чётная неделя, {week} по счёту')
    elif week % 2 != 0:
        bot.send_message(message.chat.id, f'Сейчас идёт нечётная неделя, {week} по счёту')
@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда вам сюда - https://mtuci.ru/')
    elif message.text.lower() == 'понедельник':
        send_Monday(message)
    elif message.text.lower() == 'вторник':
        send_Tuesday(message)
    elif message.text.lower() == 'среда':
        send_Wednesday(message)
    elif message.text.lower() == 'четверг':
        send_Thursday(message)
    elif message.text.lower() == 'пятница':
        send_Friday(message)
    elif message.text.lower() == 'суббота':
        send_Saturday(message)
    elif message.text.lower() == 'расписание на текущую неделю':
        send_timetable_to_this_week(message)
    elif message.text.lower() == 'расписание на следующую неделю':
        send_timetable_to_next_week(message)
    elif message.text.lower() == 'выход в главное меню':
        exit(message)
    elif message.text.lower() == 'текущая неделя':
        give_week(message)
    elif message.text.lower() == 'сайт нашего вуза':
        give_website(message)
    elif message.text.lower() == 'привет' or 'здравствуйте':
        send_Hello(message)
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')
@bot.message_handler(commands=['hello'])
def send_Hello(message):
    bot.send_message(message.chat.id,'Здравствуйте!!! Я очень сильно хочу быть полезным для вас, поэтому не стесняйтесь и нажимайте все те кнопки, которые вам нужны.',reply_markup=keyboard_menu)
@bot.message_handler(commands=['website'])
def give_website(message):
    bot.send_message(message.chat.id,'https://mtuci.ru/', reply_markup=keyboard_menu)

@bot.message_handler(commands=['Monday'])
def send_Monday(message):
    b = ''
    if week % 2 == 0:
        cursor.execute("SELECT * FROM timetable2 WHERE day='Monday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______'  + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание в понедельник:\n\n{correct_answer+st}')
    elif week % 2 != 0:
        cursor.execute("SELECT * FROM timetable1 WHERE day='Monday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание в понедельник:\n\n{correct_answer+st}')
@bot.message_handler(commands=['Tuesday'])
def send_Tuesday(message):
    b = ''
    if week % 2 == 0:
        cursor.execute("SELECT * FROM timetable2 WHERE day='Tuesday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание во вторник:\n\n{correct_answer+st}')
    elif week % 2 != 0:
        cursor.execute("SELECT * FROM timetable1 WHERE day='Tuesday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание во вторник:\n\n{correct_answer+st}')

@bot.message_handler(commands=['Wednesday'])
def send_Wednesday(message):
    b = ''
    if week % 2 == 0:
        cursor.execute("SELECT * FROM timetable2 WHERE day='Wednesday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание в среду:\n\n{correct_answer+st}')
    elif week % 2 != 0:
        cursor.execute("SELECT * FROM timetable1 WHERE day='Wednesday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание в среду:\n\n{correct_answer+st}')

@bot.message_handler(commands=['Thursday'])
def send_Thursday(message):
    b = ''
    if week % 2 == 0:
        cursor.execute("SELECT * FROM timetable2 WHERE day='Thursday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание в четверг:\n\n{correct_answer+st}')
    elif week % 2 != 0:
        cursor.execute("SELECT * FROM timetable1 WHERE day='Thursday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание в четверг:\n\n{correct_answer+st}')
@bot.message_handler(commands=['Friday'])
def send_Friday(message):
    b = ''
    if week % 2 == 0:
        cursor.execute("SELECT * FROM timetable2 WHERE day='Friday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, ваше расписание в пятницу:\n\n{correct_answer+st}')
    elif week % 2 != 0:
        bot.send_message(message.chat.id,f'Сейчас идёт {week} неделя, и так как она нечётная, пар в пятницу у вас нет.')
@bot.message_handler(commands=['Saturday'])
def send_Saturday(message):
    b = ''
    if week % 2 == 0:
        cursor.execute("SELECT * FROM timetable2 WHERE day='Saturday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт чётная {week} неделя, ваше расписание в субботу:\n\n{correct_answer+st}')
    else:
        cursor.execute("SELECT * FROM timetable1 WHERE day='Saturday'")
        records = list(cursor.fetchall())
        correct_answer = records[0][1].strip() + '\n' + '_______' + '\n'
        a = []
        b = []
        for i in range(len(records)):
            a = [i for i in records[i][2:]]
            for i in a:
                b.append(i)
        st = ''
        count_of_space = 0
        for i in b:
            st += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st += '\n'
            else:
                continue
        st = '\n' + st + '_______'
        bot.send_message(message.chat.id,f'Сейчас идёт нечётная {week} неделя, ваше расписание в субботу:\n\n{correct_answer+st}')


@bot.message_handler(commands=['timetable_to_this_week'])
def send_timetable_to_this_week(message):
    if week % 2 != 0:
        cursor.execute("SELECT * FROM timetable1")
        records = list(cursor.fetchall())
        timetable_in_Monday = []
        a1 = []
        b1 = []

        timetable_in_Tuesday = []
        a2 = []
        b2 = []

        timetable_in_Wednesday = []
        a3 = []
        b3 = []

        timetable_in_Thursday = []
        a4 = []
        b4 = []
        timetable_in_Friday = []


        timetable_in_Saturday = []
        a6 = []
        b6 = []

        for i in range(len(records)):
            if records[i][1] == 'Monday':
                timetable_in_Monday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Tuesday':
                timetable_in_Tuesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Wednesday':
                timetable_in_Wednesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Thursday':
                timetable_in_Thursday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Friday':
                timetable_in_Friday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Saturday':
                timetable_in_Saturday.append(records[i])

        day_of_week1 = timetable_in_Monday[0][1]
        correct_answer1 = day_of_week1 + '\n' + '_______'

        day_of_week2 = timetable_in_Tuesday[0][1]
        correct_answer2 = day_of_week2 + '\n' + '_______'

        day_of_week3 = timetable_in_Wednesday[0][1]
        correct_answer3 = day_of_week3 + '\n' + '_______'

        day_of_week4 = timetable_in_Thursday[0][1]
        correct_answer4 = day_of_week4 + '\n' + '_______'

        day_of_week5 = ''
        correct_answer5 = 'Friday' + '\n' + '_______'

        day_of_week6 = timetable_in_Saturday[0][1]
        correct_answer6 = day_of_week6 + '\n' + '_______'


        for i in range(len(timetable_in_Monday)):
            a1 = [i for i in timetable_in_Monday[i][2:]]
            for i in a1:
                b1.append(i)
        st1 = ''
        count_of_space = 0
        for i in b1:
            st1 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st1 += '\n'
            else:
                continue
        st1 = '\n' + st1 + '_______'
        result1 = correct_answer1 + '\n' + st1 + '\n' + '\n'


        for i in range(len(timetable_in_Tuesday)):
            a2 = [i for i in timetable_in_Tuesday[i][2:]]
            for i in a2:
                b2.append(i)
        st2 = ''
        count_of_space = 0
        for i in b2:
            st2 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st2 += '\n'
            else:
                continue
        st2 = '\n' + st2 + '_______'
        result2 = correct_answer2 + '\n' + st2 + '\n' + '\n'


        for i in range(len(timetable_in_Wednesday)):
            a3 = [i for i in timetable_in_Wednesday[i][2:]]
            for i in a3:
                b3.append(i)
        st3 = ''
        count_of_space = 0
        for i in b3:
            st3 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st3 += '\n'
            else:
                continue
        st3 = '\n' + st3 + '_______'
        result3 = correct_answer3 + '\n' + st3 + '\n' + '\n'


        for i in range(len(timetable_in_Thursday)):
            a4 = [i for i in timetable_in_Thursday[i][2:]]
            for i in a4:
                b4.append(i)
        st4 = ''
        count_of_space = 0
        for i in b4:
            st4 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st4 += '\n'
            else:
                continue
        st4 = '\n' + st4 + '_______'
        result4 = correct_answer4 + '\n' + st4 + '\n' + '\n'


        st5 = '\n' + 'There are no pairs in this day' + '\n' + '_______'
        result5 = correct_answer5 + '\n' + st5 + '\n' + '\n'


        for i in range(len(timetable_in_Saturday)):
            a6 = [i for i in timetable_in_Saturday[i][2:]]
            for i in a6:
                b6.append(i)
        st6 = ''
        count_of_space = 0
        for i in b6:
            st6 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st6 += '\n'
            else:
                continue
        st6 = '\n' + st6 + '_______'
        result6 = correct_answer6 + '\n' + st6 + '\n' + '\n'

        overall_result = result1 + result2 + result3 + result4 + result5 + result6
        bot.send_message(message.chat.id,f'Сейчас идёт нечётная {week} неделя. Ваше текущее расписание:\n\n{overall_result}')
    else:
        cursor.execute("SELECT * FROM timetable2")
        records = list(cursor.fetchall())
        timetable_in_Monday = []
        a1 = []
        b1 = []

        timetable_in_Tuesday = []
        a2 = []
        b2 = []

        timetable_in_Wednesday = []
        a3 = []
        b3 = []

        timetable_in_Thursday = []
        a4 = []
        b4 = []

        timetable_in_Friday = []
        a5 = []
        b5 = []

        timetable_in_Saturday = []
        a6 = []
        b6 = []

        for i in range(len(records)):
            if records[i][1] == 'Monday':
                timetable_in_Monday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Tuesday':
                timetable_in_Tuesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Wednesday':
                timetable_in_Wednesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Thursday':
                timetable_in_Thursday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Friday':
                timetable_in_Friday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Saturday':
                timetable_in_Saturday.append(records[i])

        day_of_week1 = timetable_in_Monday[0][1]
        correct_answer1 = day_of_week1 + '\n' + '_______'

        day_of_week2 = timetable_in_Tuesday[0][1]
        correct_answer2 = day_of_week2 + '\n' + '_______'

        day_of_week3 = timetable_in_Wednesday[0][1]
        correct_answer3 = day_of_week3 + '\n' + '_______'

        day_of_week4 = timetable_in_Thursday[0][1]
        correct_answer4 = day_of_week4 + '\n' + '_______'

        day_of_week5 = timetable_in_Friday[0][1]
        correct_answer5 = day_of_week5 + '\n' + '_______'

        day_of_week6 = timetable_in_Saturday[0][1]
        correct_answer6 = day_of_week6 + '\n' + '_______'


        for i in range(len(timetable_in_Monday)):
            a1 = [i for i in timetable_in_Monday[i][2:]]
            for i in a1:
                b1.append(i)
        st1 = ''
        count_of_space = 0
        for i in b1:
            st1 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st1 += '\n'
            else:
                continue
        st1 = '\n' + st1 + '_______'
        result1 = correct_answer1 + '\n' + st1 + '\n' + '\n'


        for i in range(len(timetable_in_Tuesday)):
            a2 = [i for i in timetable_in_Tuesday[i][2:]]
            for i in a2:
                b2.append(i)
        st2 = ''
        count_of_space = 0
        for i in b2:
            st2 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st2 += '\n'
            else:
                continue
        st2 = '\n' + st2 + '_______'
        result2 = correct_answer2 + '\n' + st2 + '\n' + '\n'


        for i in range(len(timetable_in_Wednesday)):
            a3 = [i for i in timetable_in_Wednesday[i][2:]]
            for i in a3:
                b3.append(i)
        st3 = ''
        count_of_space = 0
        for i in b3:
            st3 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st3 += '\n'
            else:
                continue
        st3 = '\n' + st3 + '_______'
        result3 = correct_answer3 + '\n' + st3 + '\n' + '\n'


        for i in range(len(timetable_in_Thursday)):
            a4 = [i for i in timetable_in_Thursday[i][2:]]
            for i in a4:
                b4.append(i)
        st4 = ''
        count_of_space = 0
        for i in b4:
            st4 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st4 += '\n'
            else:
                continue
        st4 = '\n' + st4 + '_______'
        result4 = correct_answer4 + '\n' + st4 + '\n' + '\n'

        for i in range(len(timetable_in_Friday)):
            a5 = [i for i in timetable_in_Friday[i][2:]]
            for i in a5:
                b5.append(i)
        st5 = ''
        count_of_space = 0
        for i in b5:
            st5 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st5 += '\n'
            else:
                continue
        st5 = '\n' + st5 + '_______'
        result5 = correct_answer5 + '\n' + st5 + '\n' + '\n'

        for i in range(len(timetable_in_Saturday)):
            a6 = [i for i in timetable_in_Saturday[i][2:]]
            for i in a6:
                b6.append(i)
        st6 = ''
        count_of_space = 0
        for i in b6:
            st6 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st6 += '\n'
            else:
                continue
        st6 = '\n' + st6 + '_______'
        result6 = correct_answer6 + '\n' + st6 + '\n' + '\n'

        overall_result = result1 + result2 + result3 + result4 + result5 + result6
        bot.send_message(message.chat.id,f'Сейчас идёт чётная {week} неделя. Ваше текущее расписание:\n\n{overall_result}')
@bot.message_handler(commands=['timetable_to_next_week'])
def send_timetable_to_next_week(message):
    week_next = week + 1
    if week_next % 2 != 0:
        cursor.execute("SELECT * FROM timetable1")
        records = list(cursor.fetchall())
        timetable_in_Monday = []
        a1 = []
        b1 = []

        timetable_in_Tuesday = []
        a2 = []
        b2 = []

        timetable_in_Wednesday = []
        a3 = []
        b3 = []

        timetable_in_Thursday = []
        a4 = []
        b4 = []
        timetable_in_Friday = []


        timetable_in_Saturday = []
        a6 = []
        b6 = []

        for i in range(len(records)):
            if records[i][1] == 'Monday':
                timetable_in_Monday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Tuesday':
                timetable_in_Tuesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Wednesday':
                timetable_in_Wednesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Thursday':
                timetable_in_Thursday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Friday':
                timetable_in_Friday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Saturday':
                timetable_in_Saturday.append(records[i])

        day_of_week1 = timetable_in_Monday[0][1]
        correct_answer1 = day_of_week1 + '\n' + '_______'

        day_of_week2 = timetable_in_Tuesday[0][1]
        correct_answer2 = day_of_week2 + '\n' + '_______'

        day_of_week3 = timetable_in_Wednesday[0][1]
        correct_answer3 = day_of_week3 + '\n' + '_______'

        day_of_week4 = timetable_in_Thursday[0][1]
        correct_answer4 = day_of_week4 + '\n' + '_______'

        day_of_week5 = ''
        correct_answer5 = 'Friday' + '\n' + '_______'

        day_of_week6 = timetable_in_Saturday[0][1]
        correct_answer6 = day_of_week6 + '\n' + '_______'


        for i in range(len(timetable_in_Monday)):
            a1 = [i for i in timetable_in_Monday[i][2:]]
            for i in a1:
                b1.append(i)
        st1 = ''
        count_of_space = 0
        for i in b1:
            st1 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st1 += '\n'
            else:
                continue
        st1 = '\n' + st1 + '_______'
        result1 = correct_answer1 + '\n' + st1 + '\n' + '\n'


        for i in range(len(timetable_in_Tuesday)):
            a2 = [i for i in timetable_in_Tuesday[i][2:]]
            for i in a2:
                b2.append(i)
        st2 = ''
        count_of_space = 0
        for i in b2:
            st2 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st2 += '\n'
            else:
                continue
        st2 = '\n' + st2 + '_______'
        result2 = correct_answer2 + '\n' + st2 + '\n' + '\n'


        for i in range(len(timetable_in_Wednesday)):
            a3 = [i for i in timetable_in_Wednesday[i][2:]]
            for i in a3:
                b3.append(i)
        st3 = ''
        count_of_space = 0
        for i in b3:
            st3 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st3 += '\n'
            else:
                continue
        st3 = '\n' + st3 + '_______'
        result3 = correct_answer3 + '\n' + st3 + '\n' + '\n'


        for i in range(len(timetable_in_Thursday)):
            a4 = [i for i in timetable_in_Thursday[i][2:]]
            for i in a4:
                b4.append(i)
        st4 = ''
        count_of_space = 0
        for i in b4:
            st4 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st4 += '\n'
            else:
                continue
        st4 = '\n' + st4 + '_______'
        result4 = correct_answer4 + '\n' + st4 + '\n' + '\n'


        st5 = '\n' + 'There are no pairs in this day' + '\n' + '_______'
        result5 = correct_answer5 + '\n' + st5 + '\n' + '\n'


        for i in range(len(timetable_in_Saturday)):
            a6 = [i for i in timetable_in_Saturday[i][2:]]
            for i in a6:
                b6.append(i)
        st6 = ''
        count_of_space = 0
        for i in b6:
            st6 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st6 += '\n'
            else:
                continue
        st6 = '\n' + st6 + '_______'
        result6 = correct_answer6 + '\n' + st6 + '\n' + '\n'

        overall_result = result1 + result2 + result3 + result4 + result5 + result6
        bot.send_message(message.chat.id,f'Следующая {week_next} неделя будет нечётной. Ваше расписание на следующую неделю:\n\n{overall_result}')
    else:
        cursor.execute("SELECT * FROM timetable2")
        records = list(cursor.fetchall())
        timetable_in_Monday = []
        a1 = []
        b1 = []

        timetable_in_Tuesday = []
        a2 = []
        b2 = []

        timetable_in_Wednesday = []
        a3 = []
        b3 = []

        timetable_in_Thursday = []
        a4 = []
        b4 = []

        timetable_in_Friday = []
        a5 = []
        b5 = []

        timetable_in_Saturday = []
        a6 = []
        b6 = []

        for i in range(len(records)):
            if records[i][1] == 'Monday':
                timetable_in_Monday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Tuesday':
                timetable_in_Tuesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Wednesday':
                timetable_in_Wednesday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Thursday':
                timetable_in_Thursday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Friday':
                timetable_in_Friday.append(records[i])
        for i in range(len(records)):
            if records[i][1] == 'Saturday':
                timetable_in_Saturday.append(records[i])

        day_of_week1 = timetable_in_Monday[0][1]
        correct_answer1 = day_of_week1 + '\n' + '_______'

        day_of_week2 = timetable_in_Tuesday[0][1]
        correct_answer2 = day_of_week2 + '\n' + '_______'

        day_of_week3 = timetable_in_Wednesday[0][1]
        correct_answer3 = day_of_week3 + '\n' + '_______'

        day_of_week4 = timetable_in_Thursday[0][1]
        correct_answer4 = day_of_week4 + '\n' + '_______'

        day_of_week5 = timetable_in_Friday[0][1]
        correct_answer5 = day_of_week5 + '\n' + '_______'

        day_of_week6 = timetable_in_Saturday[0][1]
        correct_answer6 = day_of_week6 + '\n' + '_______'


        for i in range(len(timetable_in_Monday)):
            a1 = [i for i in timetable_in_Monday[i][2:]]
            for i in a1:
                b1.append(i)
        st1 = ''
        count_of_space = 0
        for i in b1:
            st1 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st1 += '\n'
            else:
                continue
        st1 = '\n' + st1 + '_______'
        result1 = correct_answer1 + '\n' + st1 + '\n' + '\n'


        for i in range(len(timetable_in_Tuesday)):
            a2 = [i for i in timetable_in_Tuesday[i][2:]]
            for i in a2:
                b2.append(i)
        st2 = ''
        count_of_space = 0
        for i in b2:
            st2 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st2 += '\n'
            else:
                continue
        st2 = '\n' + st2 + '_______'
        result2 = correct_answer2 + '\n' + st2 + '\n' + '\n'


        for i in range(len(timetable_in_Wednesday)):
            a3 = [i for i in timetable_in_Wednesday[i][2:]]
            for i in a3:
                b3.append(i)
        st3 = ''
        count_of_space = 0
        for i in b3:
            st3 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st3 += '\n'
            else:
                continue
        st3 = '\n' + st3 + '_______'
        result3 = correct_answer3 + '\n' + st3 + '\n' + '\n'


        for i in range(len(timetable_in_Thursday)):
            a4 = [i for i in timetable_in_Thursday[i][2:]]
            for i in a4:
                b4.append(i)
        st4 = ''
        count_of_space = 0
        for i in b4:
            st4 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st4 += '\n'
            else:
                continue
        st4 = '\n' + st4 + '_______'
        result4 = correct_answer4 + '\n' + st4 + '\n' + '\n'

        for i in range(len(timetable_in_Friday)):
            a5 = [i for i in timetable_in_Friday[i][2:]]
            for i in a5:
                b5.append(i)
        st5 = ''
        count_of_space = 0
        for i in b5:
            st5 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st5 += '\n'
            else:
                continue
        st5 = '\n' + st5 + '_______'
        result5 = correct_answer5 + '\n' + st5 + '\n' + '\n'

        for i in range(len(timetable_in_Saturday)):
            a6 = [i for i in timetable_in_Saturday[i][2:]]
            for i in a6:
                b6.append(i)
        st6 = ''
        count_of_space = 0
        for i in b6:
            st6 += i + ' '
            count_of_space += 1
            if count_of_space % 4 == 0:
                st6 += '\n'
            else:
                continue
        st6 = '\n' + st6 + '_______'
        result6 = correct_answer6 + '\n' + st6 + '\n' + '\n'

        overall_result = result1 + result2 + result3 + result4 + result5 + result6
        bot.send_message(message.chat.id,f'Следующая {week_next} неделя будет чётной. Ваше расписание на следующую неделю:\n\n{overall_result}')


bot.polling()
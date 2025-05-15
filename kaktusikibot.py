from telebot
from telebot import types
import sqlite3

#name = None

bot = telebot.Telebot('7712082869:AAHOz8CKWPEq6Ykad2wuzfpDeRABNG8z0mE')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('baza.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXIST users(id int auto_increment primary key, name varchar (50), pass varchar (50))')
    conn.commit()
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("?Задать вопрос")
    markup.add(btn1,btn2)
    bot.send_message(message.chat.id, text="Привет,{0.first_name}! Я бот, соориентирующий по кактусам".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Поздороваться"):
        bot.send_message(message.chat.id, text="Привет, рад тебя видеть!")
    elif(message.text == "?Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Зарегистрироваться на сайте")
        btn2 = types.KeyboardButton("Расскажи о ассортименте")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn1,back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
        
    elif(message.text == "Зарегистрироваться на сайте"):
        bot.send_message(message.chat.id, "Сейчас тебя зарегистрируем, как тебя зовут?")
        bot.register_next_step_handler(message, user_name)

        def user_name(message):
            global name
            name = message.text.strip()
            bot.send_message(message.chat.id, "Придумай пароль")
            bot.register_next_step_handler(message,user_pass)

        def user_pass(message):
            password = message.text.strip()
            conn = sqlite3.connect('baza.sql')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO users(name, pass) VALUES ({name},{password})')
            conn.comit()
            cur.close()
            conn.close()

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
            bot.send_message(message.chat.id, 'Ты зареган:)', reply_markup=markup)

    elif message.text == "Расскажи об ассортименте":
        bot.send_message(message.chat.id, text="Делаю вид, что рассказываю об ассортименте")

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("?Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id text="Вы вернулись в главное меню" reply_markup=markup)
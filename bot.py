import telebot
from telebot import types


class Task:
    is_running = False

    def __init__(self):
        return


# main variables
TOKEN = "467191582:AAE7pMpdGsPULVRFyhf7Vk3kYwv8VeXfV4k"
bot = telebot.TeleBot(TOKEN)
task = Task()


@bot.message_handler(commands=['start'])
def start_handler(message):
    if not task.is_running:
        bot.send_message(message.chat.id, 'Привет, скоро я заработаю')


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Красиво.')


@bot.message_handler(commands=['age'])
def age_handler(message):
    if not task.is_running:
        chat_id = message.chat.id

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('18', '19')

        msg = bot.send_message(chat_id, 'Сколько вам лет?', reply_markup=markup)
        bot.register_next_step_handler(msg, ask_age)
        task.is_running = True


def ask_age(message):
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Возраст должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, ask_age)
        return

    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id, 'Спасибо, я запомнил что вам ' + text + ' лет.', reply_markup=markup)
    task.is_running = False


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# бот находится в режиме ожидания ответа
bot.polling(none_stop=True)

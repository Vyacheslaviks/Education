import telebot
import requests
import bs4

from telebot import types


TOKEN = '6255861372:AAHA84tKwu0kKKgZZDrcdTpxny8_xM2SJ-I'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую. Вы находитесь в телеграмм-боте, который отображает погоду аэропортах в специальном формате.\n'
                     + 'Для получения иснтрукций по использованию вы можете обратится в раздел "Помощь"')
    main_menu(message)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Узнать погоду':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bt_main_menu = types.KeyboardButton('Выйти в главное меню')
        markup.add(bt_main_menu)

        msg = bot.send_message(message.chat.id, 'Введите какое-нибудь сообщение', reply_markup=markup)
        bot.register_next_step_handler(msg, get_weather)
    elif message.text == 'Помощь':
        get_help(message)
    elif message.text == 'Выйти в главное меню':
        main_menu(message)
    else:
        bot.send_message(message.chat.id, 'Не совсем вас понял')
        main_menu(message)


def get_weather(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_main_menu = types.KeyboardButton('Выйти в главное меню')
    markup.add(bt_main_menu)

    bot.send_message(message.chat.id, f'{message.text}', reply_markup=markup)

    req_airport = message.text
    url = 'https://metartaf.ru/' + req_airport
    response = requests.get(url)

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        report = soup.find_all('pre')
        report = str(report)

        start_metar = report.find('<pre>')
        end_metar = report.find('</pre>')
        metar_code = report[start_metar + 5 : end_metar]

        start_taf = report.find('<pre>', end_metar + 7)
        end_taf = report.find('</pre>', end_metar + 7)
        taf_code = report[start_taf + 5 : end_taf]

        bot.send_message(message.chat.id, f'Текущая погода (METAR):\n{metar_code}\n\nПрогноз погоды (TAF):\n{taf_code}')

        main_menu(message)

    elif message.text == 'Выйти в главное меню':
        main_menu(message)

    else:
        repeat_message = bot.send_message(message.chat.id, 'Не смог вас понять, повторите ввод')
        bot.register_next_step_handler(repeat_message, get_weather)


def get_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_main_menu = types.KeyboardButton('Выйти в главное меню')
    markup.add(bt_main_menu)

    bot.send_message(message.chat.id, 'Бот предоставляет информацию о погоде в крупных аэропортах СНГ, взятой с сайта: "https://metartaf.ru/".\n' 
                     + 'Для корректной работы необходимо ввести ИКАО-код аэропорта, вот список наиболее частых:\n'
                     + 'Москва, Шереметьево - UUEE\nМосква, Домодедово - UUDD\nМосква, Внуково - UUWW\n'
                     + 'Санкт-Петербург, Пулково - ULLI\nСочи, Адлер - URSS\nЕкатеринбург, Кольцово - USSS\n'
                     + 'Новосибирск, Толмачево - UNNT.\n\nДля получения полного списка аэропртов, можете обратится на сайт\n\n'
                     + 'Для расшифровки формализованных сообщений METAR и TAF, можете обратится к специальным сервисам в сети интернет.', reply_markup=markup)


def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_weather = types.KeyboardButton('Узнать погоду')
    bt_help = types.KeyboardButton('Помощь')

    markup.add(bt_weather, bt_help)
    bot.send_message(message.chat.id, 'Вы в главном меню. Выберите дальнейшее действие', reply_markup=markup)


bot.polling()
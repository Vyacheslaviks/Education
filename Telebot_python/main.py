import telebot
import requests
import bs4

from telebot import types


TOKEN = '6255861372:AAHA84tKwu0kKKgZZDrcdTpxny8_xM2SJ-I'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Првиетствую')
    main_menu(message)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Узнать погоду':
        bot.send_message(message.chat.id, 'Введите какое-нибудь сообщение')
        bot.register_next_step_handler(message, get_weather)
    elif message.text == 'Помощь':
        get_help(message)
    elif message.text == 'Выйти в главное меню':
        main_menu(message)
    else:
        bot.send_message(message.chat.id, 'Не совсем вас понял')


def get_weather(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_main_menu = types.KeyboardButton('Выйти в главное меню')
    markup.add(bt_main_menu)

    bot.send_message(message.chat.id, f'Вы ввели {message.text}', reply_markup=markup)


def get_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_main_menu = types.KeyboardButton('Выйти в главное меню')
    markup.add(bt_main_menu)

    bot.send_message(message.chat.id, 'Вы выбрали помощь', reply_markup=markup)


def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_weather = types.KeyboardButton('Узнать погоду')
    bt_help = types.KeyboardButton('Помощь')

    markup.add(bt_weather, bt_help)
    bot.send_message(message.chat.id, 'Вы в главном меню. Выберите действие', reply_markup=markup)


bot.polling()
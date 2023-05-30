import telebot
import requests
import bs4


TOKEN = '6255861372:AAHA84tKwu0kKKgZZDrcdTpxny8_xM2SJ-I'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Првиетствую')


bot.polling()
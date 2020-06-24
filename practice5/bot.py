# -*- coding: utf-8 -*-
import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(func = lambda message: True, content_types = ['text'])
def receive_message(message):
    bot.send_message(message.chat.id, f'Количество символов в сообщении - {len(message.text)}', reply_to_message_id=message.message_id)
    

if __name__ == "__main__":
    bot.infinity_polling()
# -*- coding: utf-8 -*-
import config
import utils
import telebot
from collections import namedtuple
from random import choice, seed

bot = telebot.TeleBot(config.token)

user = namedtuple('User',('id','score','guessed_riddles_id'))
riddle = namedtuple('Riddle',('id','text','correct_answer','wrong_answers'))
users = []
riddles = [
    riddle(1,'Человек хочет, чтобы он включился. Но когда он включается, человек злится и старается сразу его выключить','Будильник','Телевизор,Светофор,Телефон'),
    riddle(2,'Загадка 2','Ответ 1','Ответ 2,Ответ 3,Ответ 4'),
    riddle(3,'Загадка 3','Ответ 3','Ответ 1,Ответ 2,Ответ 4')
]


def is_user_in_list(id):
    for u in users:
        if u.id == id:
            return True
    return False

def add_user_in_list(id):
    new_user = user(id, 0, [])
    users.append(new_user)

def get_user_by_id(id):
    for u in users:
        if u.id == id:
            return u
    return None

def remove_riddle_by_ids(ids):
    new_riddles = riddles
    for r in riddles:
        for i in ids:
            if r.id == i:
                new_riddles.remove(r)
    return new_riddles

def get_random_riddle_to_user(user_id):
    curr_user = get_user_by_id(user_id)
    riddles_for_user = riddles
    if curr_user is not None:
        riddles_for_user = remove_riddle_by_ids(curr_user.guessed_riddles_id)
    return choice(riddles_for_user)

# @bot.message_handler(content_types = ['text'])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.json['text'])
@bot.message_handler(commands = ['play'])
def start_game(message):
    #if is_user_in_list(message.chat.id):
    #    continue_game(message)
    #else:
    #    add_user_in_list(message.chat.id)

    # Подключаемся к БД
    #db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    row = get_random_riddle_to_user(message.chat.id)
    # Формируем разметку
    markup = utils.generate_keyboard(row.correct_answer, row.wrong_answers)
    # Отправляем аудиофайл с вариантами ответа
    #bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    bot.send_message(message.chat.id, row.text, reply_markup=markup)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row.correct_answer)
    # Отсоединяемся от БД
    #db_worker.close()


@bot.message_handler(func = lambda message: True, content_types = ['text'])
def continue_game(message):
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, введите команду /play')
    else:
        # Уберем клавиатуру с вариантами ответа.
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        # Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id)

if __name__ == "__main__":
    seed()
    bot.infinity_polling()
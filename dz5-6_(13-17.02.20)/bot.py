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
    new_user = user(id=id, score=0, guessed_riddles_id=[])
    users.append(new_user)

# def add_guessed_riddle(riddle_id, user_id):
#     user = get_user_by_id(user_id)
#     user.score += 1
#     user.guessed_riddles_id.append(riddle_id)

def get_user_by_id(id):
    for u in users:
        if u.id == id:
            return u
    return None

def add_user_score(user_id):
    userd = get_user_by_id(user_id)
    new_user = user(id=userd.id, score=userd.score+1, guessed_riddles_id=userd.guessed_riddles_id)
    if user is not None:
        userd = new_user
    else: print(f'{__name__} - variable "user" is None')

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
    if riddles_for_user is []:
        return None
    else:
        random_riddle = choice(riddles_for_user)
        curr_user.guessed_riddles_id.append(random_riddle.id)
        return random_riddle

# @bot.message_handler(content_types = ['text'])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.json['text'])
@bot.message_handler(commands = ['play', 'score'])
def start_game(message):
    if message.json['text'] == '/score':
        get_score(message)
        return
    #if is_user_in_list(message.chat.id):
    #    continue_game(message)
    #else:
    #    add_user_in_list(message.chat.id)

    # Подключаемся к БД
    #db_worker = SQLighter(config.database_name)
    user = get_user_by_id(message.chat.id)
    if user is None:
        add_user_in_list(message.chat.id)
    # Получаем случайную строку из БД
    row = get_random_riddle_to_user(message.chat.id)
    if row is None:
        bot.send_message(message.chat.id, 'Все загадки отгаданы! Поздравляем!')
        return
    # Формируем разметку
    markup = utils.generate_keyboard(row.correct_answer, row.wrong_answers)
    # Отправляем аудиофайл с вариантами ответа
    #bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    bot.send_message(message.chat.id, row.text, reply_markup=markup)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row.correct_answer)
    

    # Отсоединяемся от БД
    #db_worker.close()



def get_score(message):
    user = get_user_by_id(message.chat.id)
    if user is not None:
        bot.send_message(message.chat.id, f'Ваш счёт - {user.score}')
    else:
        bot.send_message(message.chat.id, 'Вы ещё ни разу не сыграли!')


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
            add_user_score(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        # Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id)

if __name__ == "__main__":
    seed()
    bot.infinity_polling()
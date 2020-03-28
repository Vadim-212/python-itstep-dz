# -*- coding: utf-8 -*-
import config
import utils
import telebot
from collections import namedtuple
from random import choice, seed

bot = telebot.TeleBot(config.token)

user = namedtuple('User',('id','score','guessed_riddles_id','curr_riddle_id'))
riddle = namedtuple('Riddle',('id','text','correct_answer','wrong_answers'))
users = []
riddles = [
    riddle(1,'Человек хочет, чтобы он включился. Но когда он включается, человек злится и старается сразу его выключить','Будильник','Телевизор,Светофор,Телефон'),
    riddle(2,'Кто говорит на всех языках?','Эхо','Полиглот,Всезнайка,Мудрец'),
    riddle(3,'Что можно приготовить, но съесть нельзя?','Домашнее задание','Обед,Пирожное,Еда')
]


def is_user_in_list(id):
    for u in users:
        if u.id == id:
            return True
    return False

def add_user_in_list(id):
    new_user = user(id=id, score=0, guessed_riddles_id=[], curr_riddle_id=0)
    users.append(new_user)

def get_user_by_id(id):
    for u in users:
        if u.id == id:
            return u
    return None

def add_user_score(user_id):
    userd = get_user_by_id(user_id)
    
    new_user = user(id=userd.id, score=userd.score+1, guessed_riddles_id=userd.guessed_riddles_id, curr_riddle_id=userd.curr_riddle_id)
    if user is not None:
        users[users.index(userd)] = new_user
    else: print(f'{__name__} - variable "user" is None')

def remove_riddle_by_ids(ids):
    new_riddles = []
    new_riddles[:] = riddles[:]
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
    if riddles_for_user == []:
        return None
    else:
        random_riddle = choice(riddles_for_user)
        new_user = user(id=curr_user.id, score=curr_user.score, guessed_riddles_id=curr_user.guessed_riddles_id, curr_riddle_id=random_riddle.id)
        users[users.index(curr_user)] = new_user
        return random_riddle

def add_current_riddle_to_guessed(user_id):
    curr_user = get_user_by_id(user_id)
    curr_user.guessed_riddles_id.append(curr_user.curr_riddle_id)

def reset_all(user_id):
    curr_user = get_user_by_id(user_id)
    if curr_user is None:
        return 'Вы ещё ни разу не сыграли!'
    new_user = user(id=id, score=0, guessed_riddles_id=[], curr_riddle_id=0)
    users[users.index(curr_user)] = new_user
    return 'Текущий счёт сброшен!'

@bot.message_handler(commands = ['play', 'score', 'reset', 'help'])
def start_game(message):
    if message.json['text'] == '/help':
        string = '/play - играть/показать загадку\n/score - текущий счёт\n/reset - сброс счёта\n/help - выводит текущее сообщение'
        bot.send_message(message.chat.id, string)
    elif message.json['text'] == '/score':
        get_score(message)
    elif message.json['text'] == '/reset':
        bot.send_message(message.chat.id, reset_all(message.chat.id))
    elif message.json['text'] == '/play':
        user = get_user_by_id(message.chat.id)
        if user is None:
            add_user_in_list(message.chat.id)
        row = get_random_riddle_to_user(message.chat.id)
        if row == None:
            bot.send_message(message.chat.id, 'Все загадки отгаданы! Поздравляем!')
            return
        markup = utils.generate_keyboard(row.correct_answer, row.wrong_answers)
        bot.send_message(message.chat.id, row.text, reply_markup=markup)
        utils.set_user_game(message.chat.id, row.correct_answer)    

def get_score(message):
    user = get_user_by_id(message.chat.id)
    if user is not None:
        bot.send_message(message.chat.id, f'Ваш счёт - {user.score}')
    else:
        bot.send_message(message.chat.id, 'Вы ещё ни разу не сыграли!')


@bot.message_handler(func = lambda message: True, content_types = ['text'])
def continue_game(message):
    if message.text[0] == '/':
        bot.send_message(message.chat.id, 'Такой команды не существует!\nКоманда /help - вывод описания доступных команд.')
        return
    answer = utils.get_answer_for_user(message.chat.id)
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, введите команду /play')
    else:
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
            add_current_riddle_to_guessed(message.chat.id)
            add_user_score(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        utils.finish_user_game(message.chat.id)

if __name__ == "__main__":
    seed()
    bot.infinity_polling()
import shelve
from random import shuffle
from config import shelve_name
from telebot import types


def generate_keyboard(correct_answer, wrong_answers):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    all_answers = '{},{}'.format(correct_answer,wrong_answers)
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup


def set_user_game(chat_id, estimated_answer):
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None
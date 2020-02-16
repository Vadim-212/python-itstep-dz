from collections import namedtuple
from os import path

users = []
user = namedtuple('user',('name','birth_year','activity','favourite_movies'))
isExit = False

def help():
    print('\n\nhelp - выводит данное сообщение\n\ncreate-user - добавить пользователя\n\nshow-users - выводит всех существующих пользователей\n\nexport {путь к файлу}.csv - экспорт всех пользователей в файл csv \n\nexit - выход\n\n')

def check_activity(activity):
    if activity.lower() == 'да' or activity.lower() == 'нет':
        return activity
    else:
        return 'нет'

def get_birth_year():
    while True:
        try:
            birth_year = int(input('Введите год рождения: '))
            break
        except ValueError:
            print('Неверный год рождения!')
    return birth_year


def create_user():
    name = input('Введите имя: ')
    birth_year = get_birth_year()
    activity = check_activity(input('Пользователь активен (да/нет): '))
    favourite_movies = []
    for i in range(3):
        favourite_movies.append(input(f'Введите любимый фильм {i + 1}: '))
    users.append(user(name=name,birth_year=birth_year,activity=activity,favourite_movies=favourite_movies))
    

def show_users():
    for i in range(len(users)):
        print(f"Пользователь {i + 1}: Имя - {users[i].name}; Год рождения - {users[i].birth_year}; Активен - {users[i].activity}; Любимые фильмы - {', '.join(users[i].favourite_movies)}\n")

def export(file_name):
    with open(file_name, 'w', encoding='ansi') as f:
        f.write('N;Имя;Год рождения;Активен;Любимые фильмы;\n')
        for i in range(len(users)):
            #f.write(''.join([f'Пользователь {i + 1}:\nИмя - {users[i].name}\nГод рождения - {users[i].birth_year}']))
            f.write(f"{i + 1};{users[i].name};{users[i].birth_year};{users[i].activity};{', '.join(users[i].favourite_movies)};\n")

def exit():
    global isExit
    isExit = True

def check_file(file_name):
    if len(file_name) >= 5 and file_name[-4:] == '.csv':
        return file_name
    else:
        return 'info.csv'


while isExit is not True:
    query = input('Введите: ')
    if query == 'create-user':
        create_user()
    elif query == 'show-users':
        show_users()
    elif 'export' in query:
        export(check_file(query[7:]))
    elif query == 'exit':
        exit()
    else:
        help()

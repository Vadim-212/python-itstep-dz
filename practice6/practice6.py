from collections import namedtuple
from os import path
import sqlite3

db_exist = path.exists('usersdb.sqlite3')

conn = sqlite3.connect('usersdb.sqlite3')

user = namedtuple('user',('name','birth_year','activity','favourite_movies'))
isExit = False

def create_db(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth_year INTEGER NOT NULL,
            activity INTEGER 
        );""")
    cursor.execute("""CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );""")
    cursor.execute("""CREATE TABLE users_movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(movie_id) REFERENCES movies(id) 
        );""")

if not db_exist:
    create_db(conn)

def add_user_to_db(connection, user):
    cursor = connection.cursor()
    name = user.name
    birth_year = user.birth_year
    activity = 0
    if user.activity == 'да':
        activity = 1
    favourite_movies = user.favourite_movies
    for movie in favourite_movies:
        cursor.execute('INSERT INTO movies (name) VALUES (?)', (movie,))
    cursor.execute('INSERT INTO users (name,birth_year,activity) VALUES (?,?,?)', (name, birth_year, activity,))
    for movie in favourite_movies:
        row_user = cursor.execute('SELECT id FROM users WHERE name=? AND birth_year=?', (name, birth_year,)).fetchone()
        row_movie = cursor.execute('SELECT id FROM movies WHERE name=?', (movie,)).fetchone()
        cursor.execute('INSERT INTO users_movies (user_id,movie_id) VALUES (?,?)', (row_user[0], row_movie[0],))
        
    connection.commit()


def help():
    print('\n\nhelp - выводит данное сообщение\n\ncreate-user - добавить пользователя\n\nshow-users - выводит всех существующих пользователей\n\nexit - выход\n\n')

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
    new_user = user(name=name,birth_year=birth_year,activity=activity,favourite_movies=favourite_movies)
    add_user_to_db(conn, new_user)
    

def show_users():
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM users'):
        user_movies_rows = cursor.execute('SELECT m.name FROM movies m JOIN users_movies um ON um.movie_id=m.id WHERE um.user_id=?', (row[0],)).fetchall()
        user_movies = []
        for movie in user_movies_rows:
            user_movies.append(movie[0])
        print(f"Пользователь: Имя - {row[1]}; Год рождения - {row[2]}; Активен - {row[3]}; Любимые фильмы - {', '.join(user_movies)}\n")

def exit():
    global isExit
    isExit = True


while isExit is not True:
    query = input('Введите: ')
    if query == 'create-user':
        create_user()
    elif query == 'show-users':
        show_users()
    elif query == 'exit':
        exit()
        conn.close()
    else:
        help()

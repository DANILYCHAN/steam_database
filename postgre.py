import psycopg2
from config import host, user, password, db_name
import random
import string
from datetime import datetime as DT
from datetime import timedelta
from faker import Faker
import requests

fake = Faker()

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def get_random_date(start, end):
    delta = end - start
    return start + timedelta(random.randint(0, delta.days))

start_dt = DT.strptime('01.01.2005', '%d.%m.%Y')
end_dt = DT.strptime('01.01.2022', '%d.%m.%Y')

"""
games = open("Igry.txt")
name = games.readlines()

publishers = open("Izdateli_igr.txt")
publisher = publishers.readlines()

developers = open("Razrabot.txt")
developer = developers.readlines()

genres = open('genres.txt')
tag_info = genres.readlines()
"""
tag_list = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
games_list = list(range(1, 100))

try:
    # connection to exist database 
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    connection.autocommit = True

    # the cursor for perfoming database operations
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT VERSION()"
        )

        print(f"Server version: {cursor.fetchone()}")

        '''
        with connection.cursor() as cursor:
            for i in range(100):
                price = random.randint(1, 75)
                rating = random.randint(1, 10)
                date = get_random_date(start_dt, end_dt).strftime("%d.%m.%Y")
                cursor.execute(
                    f"""INSERT INTO game (name, developer, publisher, price, rating, release_date) 
                    VALUES ('{name[i]}', '{developer[i]}', '{publisher[i]}', {price}, {rating}, '{date}')"""
                )
        
        with connection.cursor() as cursor:
            for i in range(12):
                cursor.execute(
                    f"""INSERT INTO tag (tag_info) 
                    VALUES ('{tag_info[i]}')"""
                )
        
        with connection.cursor() as cursor:
            for i in range(1, 100):
                choice = random.sample(tag_list, 2)

                for j in range(2):
                    cursor.execute(
                        f"""INSERT INTO game_tag_link (tag_id, game_id) 
                        VALUES ({choice[j]}, {i+1})"""
                    )
        
        with connection.cursor() as cursor:
            for i in range(97):
                login = generate_random_string(random.randint(3, 20))
                password = generate_random_string(random.randint(8, 50))
                nickname = generate_random_string(random.randint(1, 30))
                profile_lvl = random.randint(0, 255)
                balance = random.randint(0, 10000)
                avatar = requests.get('https://picsum.photos/184/184')
                cursor.execute(
                    f"""INSERT INTO user_data (login, password, nickname, profile_lvl, balance, avatar) 
                    VALUES ('{login}', '{password}', '{nickname}', {profile_lvl}, {balance}, '{avatar.url}')"""
                )
        
        with connection.cursor() as cursor:
            for i in range(99):
                rating = random.randint(1, 10)
                date = get_random_date(start_dt, end_dt).strftime("%d.%m.%Y")
                cursor.execute(
                    f"""INSERT INTO review (user_id, game_id, review_date, review_text, rating) 
                    VALUES ({random.randint(1, 100)}, {random.randint(1, 100)}, '{date}', '{fake.text(max_nb_chars=290)}', {rating})"""
                )

        with connection.cursor() as cursor:
            for i in range(10):
                choice = random.sample(games_list, random.randint(1, 4))

                for j in choice:
                    cursor.execute(
                        f"""INSERT INTO user_game_link (user_id, game_id) 
                        VALUES ({i+11}, {j})"""
                    )
        '''
        
        print("[INFO] Succesfully inserted")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection: 
        connection.close()
        print("[INFO] PostgreSQL connection closed")
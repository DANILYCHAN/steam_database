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

games = open("Igry.txt")
name = games.readlines()

publishers = open("Izdateli_igr.txt")
publisher = publishers.readlines()

developers = open("Razrabot.txt")
developer = developers.readlines()

genres = open('genres.txt')
tag_info = genres.readlines()

tag_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
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
            for i in range(100):
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
            for i in range(100):
                rating = random.randint(1, 10)
                date = get_random_date(start_dt, end_dt).strftime("%d.%m.%Y")
                cursor.execute(
                    f"""INSERT INTO review (user_id, game_id, review_date, review_text, rating) 
                    VALUES ({random.randint(1, 100)}, {random.randint(1, 100)}, '{date}', '{fake.text(max_nb_chars=290)}', {rating})"""
                )
        
        with connection.cursor() as cursor:
            for i in range(100):
                choice = random.sample(games_list, random.randint(1, 3))

                for j in choice:
                    cursor.execute(
                        f"""INSERT INTO user_game_link (user_id, game_id) 
                        VALUES ({i+1}, {j})"""
                    )
        
        with connection.cursor() as cursor:
            for i in range(100):
                item_name = generate_random_string(random.randint(3, 8))
                cursor.execute(
                    f"""INSERT INTO cosmetic_items (game_id, name) 
                    VALUES ({i+1}, '{item_name}')"""
                )

        with connection.cursor() as cursor:
            for i in range(100):
                amount = random.randint(1, 10)
                item_name = generate_random_string(random.randint(3, 8))
                cursor.execute(
                    f"""INSERT INTO cosmetic_user_link (user_id, cosmetic_item_id, amount) 
                    VALUES ({i+1}, {i+1}, {amount})"""
                )
        
        with connection.cursor() as cursor:
            for i in range(100):
                ingame_purchase_name = generate_random_string(random.randint(5, 10))
                price = random.randint(0, 100)
                cursor.execute(
                    f"""INSERT INTO ingame_purchase (game_id, price, name) 
                    VALUES ({i+1}, {price},'{ingame_purchase_name}')"""
                )
        
        with connection.cursor() as cursor:
            for i in range(100):
                cursor.execute(
                    f"""INSERT INTO ingame_purchase_user_link (ingame_purchase_id, user_id) 
                    VALUES ({i+1}, {i+1})"""
                )

        print("[INFO] Succesfully inserted")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection: 
        connection.close()
        print("[INFO] PostgreSQL connection closed")
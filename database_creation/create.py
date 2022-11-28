import psycopg2
from config import host, user, password, db_name

database_name = 'steam_0'

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
            cursor.execute(
                f"""CREATE DATABASE {database_name}
                    WITH
                    OWNER = postgres
                    ENCODING = 'UTF8'
                    LC_COLLATE = 'Russian_Russia.1251'
                    LC_CTYPE = 'Russian_Russia.1251'
                    TABLESPACE = pg_default
                    CONNECTION LIMIT = -1
                    IS_TEMPLATE = False;"""
            )
        
        print("[INFO] Succesfully created")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection: 
        connection.close()
        print("[INFO] PostgreSQL connection closed")



try:
    # connection to exist database 
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )

    connection.autocommit = True

    # the cursor for perfoming database operations
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT VERSION()"
        )

        print(f"Server version: {cursor.fetchone()}")

        with connection.cursor() as cursor:
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS public.game
                        (
                            id serial primary key,
                            name character varying(255) COLLATE pg_catalog."default" NOT NULL,
                            developer character varying(255) COLLATE pg_catalog."default" NOT NULL,
                            publisher character varying(255) COLLATE pg_catalog."default" NOT NULL,
                            price integer,
                            rating integer NOT NULL,
                            release_date character varying(10) COLLATE pg_catalog."default"
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.game
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.user_data
                        (
                            id serial primary key,
                            login character varying(30) COLLATE pg_catalog."default" NOT NULL,
                            password character varying(255) COLLATE pg_catalog."default" NOT NULL,
                            nickname character varying(30) COLLATE pg_catalog."default" NOT NULL,
                            profile_lvl integer NOT NULL,
                            balance integer,
                            avatar character varying(255) COLLATE pg_catalog."default"
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.user_data
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.tag
                        (
                            id serial primary key,
                            tag_info character varying(30) COLLATE pg_catalog."default" NOT NULL
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.tag
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.review
                        (
                            id serial primary key,
                            user_id integer references user_data(id) NOT NULL,
                            game_id integer references game(id) NOT NULL,
                            review_text text COLLATE pg_catalog."default",
                            rating integer NOT NULL,
                            review_date character varying(300) COLLATE pg_catalog."default" NOT NULL
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.review
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.ingame_purchase
                        (
                            id serial primary key,
                            game_id integer references game(id) NOT NULL,
                            price integer NOT NULL,
                            name text COLLATE pg_catalog."default" NOT NULL
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.ingame_purchase
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.cosmetic_items
                        (
                            id serial primary key,
                            game_id integer references game(id) NOT NULL,
                            name character varying(255) COLLATE pg_catalog."default" NOT NULL
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.cosmetic_items
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.cosmetic_user_link
                        (
                            user_id integer references user_data(id) NOT NULL,
                            cosmetic_item_id integer references cosmetic_items(id) NOT NULL,
                            id serial primary key,
                            amount integer
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.cosmetic_user_link
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.game_tag_link
                        (
                            id serial primary key,
                            tag_id integer references tag(id) NOT NULL,
                            game_id integer references game(id) NOT NULL
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.game_tag_link
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.ingame_purchase_user_link
                        (
                            id serial primary key,
                            ingame_purchase_id integer references ingame_purchase(id) NOT NULL,
                            user_id integer references user_data(id) NOT NULL
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.ingame_puchase_user_link
                            OWNER to postgres;

                    CREATE TABLE IF NOT EXISTS public.user_game_link
                        (
                            user_id integer references user_data(id) NOT NULL,
                            game_id integer references game(id) NOT NULL,
                            id serial primary key
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.user_game_link
                            OWNER to postgres;"""        
                )
        
        print("[INFO] Succesfully created")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection: 
        connection.close()
        print("[INFO] PostgreSQL connection closed")
import psycopg2
from dotenv import load_dotenv
from os import getenv
from ipdb import set_trace

load_dotenv()

configs = {
    "host": getenv("HOST"),
    "database": getenv("DATABASE"),
    "user": getenv("USER"),
    "password": getenv("PASSWORD")
}


class Series:

    FIELDNAMES = ["id", "serie", "seasons", "released_date", "genre", "imdb_rating"]

    def __init__(self, serie: str, seasons: int, released_date: str, genre: str, imdb_rating: float) -> None:
        self.serie = serie.title()
        self.seasons = seasons
        self.released_date = released_date
        self.genre = genre.title()
        self.imdb_rating = imdb_rating

    @staticmethod
    def create_table():
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS ka_series(
                    id BIGSERIAL constraint pk_ka_series PRIMARY KEY,
                    serie VARCHAR(100) NOT NULL UNIQUE,
                    seasons INTEGER NOT NULL,
                    released_date DATE NOT NULL,
                    genre VARCHAR(50) NOT NULL,
                    imdb_rating FLOAT NOT NULL
                );
            """
        )

        conn.commit()
        cur.close()
        conn.close()

    def create(self):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        Series.create_table()

        query = """
                    INSERT INTO ka_series (serie, seasons, released_date, genre, imdb_rating)
                    VALUES (%s, %s, %s, %s, %s)
                    returning *
                """
        serie_values = list(self.__dict__.values())

        cur.execute(query, serie_values)
        new = cur.fetchone()

        conn.commit()

        cur.close()
        conn.close()

        return dict(zip(self.FIELDNAMES, new))

    @staticmethod
    def series():
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        Series.create_table()

        cur.execute(
            """
                SELECT * FROM ka_series;
            """
        )

        show_data = cur.fetchall()
        result = [dict(zip(Series.FIELDNAMES, row)) for row in show_data]

        conn.commit()

        cur.close()
        conn.close()

        return result

    @staticmethod
    def select_by_id(id):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        Series.create_table()

        cur.execute(
            """
                SELECT * FROM ka_series WHERE id=%s;
            """,
            (id,)
        )

        show_one_data = cur.fetchone()
        result = dict(zip(Series.FIELDNAMES, show_one_data))

        conn.commit()

        cur.close()
        conn.close()

        return result

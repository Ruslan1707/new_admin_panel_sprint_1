import sqlite3
from contextlib import contextmanager


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn  # С конструкцией yield вы познакомитесь в следующем модуле
        # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    # Даже если в процессе соединения произойдёт ошибка, блок finally всё равно его закроет
    finally:
        conn.close()


db_path = "db.sqlite"
with conn_context(db_path) as conn:
    curs = conn.cursor()
    curs.execute("SELECT * FROM film_work;")
    data = curs.fetchall()
    print(dict(data[0]))
# Тут соединение уже закрыто

import sqlite3
from contextlib import contextmanager

import psycopg

from .settings import POSTGRES_DSN, SQLITE_PATH


@contextmanager
def sqlite_conn():
    conn = sqlite3.connect(SQLITE_PATH)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_conn():
    with psycopg.connect(POSTGRES_DSN) as conn:
        yield conn

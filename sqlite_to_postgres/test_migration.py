from __future__ import annotations

import sqlite3
from typing import Iterable

import psycopg
import pytest

SQLITE_PATH = "db.sqlite"
POSTGRES_DSN = "postgresql://app:123qwe@localhost:5432/postgres"
TABLES = (
    "genre",
    "person",
    "film_work",
    "genre_film_work",
    "person_film_work",
)


@pytest.fixture(scope="session")
def sqlite_conn():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def pg_conn():
    with psycopg.connect(POSTGRES_DSN, row_factory=psycopg.rows.dict_row) as conn:
        yield conn


def fetch_all_sqlite(conn: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    cur = conn.execute(f"SELECT * FROM {table}")
    return cur.fetchall()


def fetch_all_pg(conn: psycopg.Connection, table: str) -> list[dict]:
    cur = conn.execute(f"SELECT * FROM content.{table}")
    return cur.fetchall()


def rows_equal(rows1: Iterable, rows2: Iterable) -> bool:
    return {tuple(r) for r in rows1} == {tuple(r.values()) for r in rows2}


@pytest.mark.parametrize("table", TABLES)
def test_row_count(table: str, sqlite_conn, pg_conn):
    assert (
        sqlite_conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        == pg_conn.execute(f"SELECT COUNT(*) FROM content.{table}").fetchone()[0]
    )


@pytest.mark.parametrize("table", TABLES)
def test_row_content(table: str, sqlite_conn, pg_conn):
    sqlite_rows = fetch_all_sqlite(sqlite_conn, table)
    pg_rows = fetch_all_pg(pg_conn, table)

    assert len(sqlite_rows) == len(pg_rows)
    assert rows_equal(sqlite_rows, pg_rows)

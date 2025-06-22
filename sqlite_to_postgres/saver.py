from typing import Any, Sequence

import psycopg


def _insert(
    pg: psycopg.Connection,
    table: str,
    columns: Sequence[str],
    rows: Sequence[Sequence[Any]],
    conflict_cols: Sequence[str],
):
    query = sql.SQL(
        """
        INSERT INTO {} ({})
        VALUES ({})
        ON CONFLICT ({}) DO NOTHING;
    """
    ).format(
        sql.Identifier(table),
        sql.SQL(",").join(map(sql.Identifier, columns)),
        sql.SQL(",").join(sql.Placeholder() * len(columns)),
        sql.SQL(",").join(map(sql.Identifier, conflict_cols)),
    )
    with pg.cursor() as cur:
        cur.executemany(query, rows)


from typing import Any, Sequence

import psycopg
from psycopg import sql


def _insert(
    pg: psycopg.Connection,
    table: str,
    columns: Sequence[str],
    rows: Sequence[Sequence[Any]],
    conflict_cols: Sequence[str],
) -> None:
    """Вставляет пачку строк с UPSERT-логикой (skip duplicates)."""

    query = sql.SQL(
        """
        INSERT INTO {table} ({cols})
        VALUES ({placeholders})
        ON CONFLICT ({conflict}) DO NOTHING;
        """
    ).format(
        table=sql.SQL(table),
        cols=sql.SQL(", ").join(map(sql.Identifier, columns)),
        placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
        conflict=sql.SQL(", ").join(map(sql.Identifier, conflict_cols)),
    )

    with pg.cursor() as cur:
        cur.executemany(query, rows)


def save_genres(pg: psycopg.Connection, batch) -> None:
    cols = ("id", "name", "description", "created", "modified")
    rows = ([r[c] for c in cols] for r in batch)
    _insert(pg, "content.genre", cols, rows, conflict_cols=("id",))


def save_persons(pg: psycopg.Connection, batch) -> None:
    cols = ("id", "full_name", "created", "modified")
    rows = ([r[c] for c in cols] for r in batch)
    _insert(pg, "content.person", cols, rows, conflict_cols=("id",))


def save_filmworks(pg: psycopg.Connection, batch) -> None:
    cols = (
        "id",
        "title",
        "description",
        "creation_date",
        "rating",
        "type",
        "created",
        "modified",
    )
    rows = ([r[c] for c in cols] for r in batch)
    _insert(pg, "content.film_work", cols, rows, conflict_cols=("id",))


def save_gfw(pg: psycopg.Connection, batch) -> None:
    cols = ("genre_id", "film_work_id", "created")
    rows = ([r[c] for c in cols] for r in batch)
    _insert(
        pg,
        "content.genre_film_work",
        cols,
        rows,
        conflict_cols=("genre_id", "film_work_id"),
    )


def save_pfw(pg: psycopg.Connection, batch) -> None:
    cols = ("person_id", "film_work_id", "role", "created")
    rows = ([r[c] for c in cols] for r in batch)
    _insert(
        pg,
        "content.person_film_work",
        cols,
        rows,
        conflict_cols=("person_id", "film_work_id", "role"),
    )

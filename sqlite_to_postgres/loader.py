import sqlite3
from typing import Iterable, Iterator, List, TypeVar

T = TypeVar("T")


def batched(cursor: Iterable[T], size: int) -> Iterator[List[T]]:
    batch: List[T] = []
    for row in cursor:
        batch.append(row)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def fetch_table(conn: sqlite3.Connection, table: str, batch: int):
    conn.row_factory = sqlite3.Row
    cur = conn.execute(f"SELECT * FROM {table};")
    for rows in batched(cur, batch):
        yield rows

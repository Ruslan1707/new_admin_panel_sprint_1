import logging

from .context import pg_conn, sqlite_conn
from .loader import fetch_table
from .saver import save_filmworks, save_genres, save_gfw, save_persons, save_pfw
from .settings import BATCH_SIZE

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)

TABLES = [
    ("genre", save_genres),
    ("person", save_persons),
    ("film_work", save_filmworks),
    ("genre_film_work", save_gfw),
    ("person_film_work", save_pfw),
]


def run():
    with sqlite_conn() as sl_conn, pg_conn() as pg:
        for table, saver in TABLES:
            logging.info("Processing table %s", table)
            for batch in fetch_table(sl_conn, table, BATCH_SIZE):
                try:
                    saver(pg, batch)
                    pg.commit()
                except Exception:
                    pg.rollback()
                    logging.exception("Failed batch from %s", table)
                    raise


if __name__ == "__main__":
    run()
    logging.info("All data migrated successfully.")

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content, public;

CREATE TABLE IF NOT EXISTS film_work (
    id            UUID PRIMARY KEY        DEFAULT uuid_generate_v4(),
    title         TEXT        NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        REAL                      CHECK (rating BETWEEN 0 AND 10),
    type          TEXT        NOT NULL,
    created       TIMESTAMPTZ NOT NULL     DEFAULT NOW(),
    modified      TIMESTAMPTZ NOT NULL     DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_film_work_creation_date ON film_work (creation_date);
CREATE INDEX IF NOT EXISTS idx_film_work_rating        ON film_work (rating);
CREATE INDEX IF NOT EXISTS idx_film_work_type          ON film_work (type);

CREATE TABLE IF NOT EXISTS genre (
    id          UUID PRIMARY KEY        DEFAULT uuid_generate_v4(),
    name        TEXT        NOT NULL,
    description TEXT,
    created     TIMESTAMPTZ NOT NULL     DEFAULT NOW(),
    modified    TIMESTAMPTZ NOT NULL     DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_genre_name  ON genre (LOWER(name));

CREATE TABLE IF NOT EXISTS person (
    id          UUID PRIMARY KEY        DEFAULT uuid_generate_v4(),
    full_name   TEXT        NOT NULL,
    created     TIMESTAMPTZ NOT NULL     DEFAULT NOW(),
    modified    TIMESTAMPTZ NOT NULL     DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_person_full_name ON person (LOWER(full_name));

CREATE TABLE IF NOT EXISTS genre_film_work (
    id           UUID PRIMARY KEY        DEFAULT uuid_generate_v4(),
    genre_id     UUID NOT NULL REFERENCES genre     (id) ON DELETE CASCADE,
    film_work_id UUID NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    created      TIMESTAMPTZ NOT NULL     DEFAULT NOW(),

    UNIQUE (genre_id, film_work_id)
);

CREATE INDEX IF NOT EXISTS idx_gfw_genre      ON genre_film_work (genre_id);
CREATE INDEX IF NOT EXISTS idx_gfw_film_work  ON genre_film_work (film_work_id);

CREATE TABLE IF NOT EXISTS person_film_work (
    id           UUID PRIMARY KEY        DEFAULT uuid_generate_v4(),
    person_id    UUID NOT NULL REFERENCES person    (id) ON DELETE CASCADE,
    film_work_id UUID NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    role         TEXT        NOT NULL,
    created      TIMESTAMPTZ NOT NULL     DEFAULT NOW(),

    UNIQUE (person_id, film_work_id, role)
);

CREATE INDEX IF NOT EXISTS idx_pfw_person     ON person_film_work (person_id);
CREATE INDEX IF NOT EXISTS idx_pfw_film_work  ON person_film_work (film_work_id);
CREATE INDEX IF NOT EXISTS idx_pfw_role       ON person_film_work (role);

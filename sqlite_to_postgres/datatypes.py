from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class Genre:
    id: UUID
    name: str
    description: Optional[str]
    created: datetime
    modified: datetime


@dataclass(slots=True)
class Person:
    id: UUID
    full_name: str
    created: datetime
    modified: datetime


@dataclass(slots=True)
class FilmWork:
    id: UUID
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    rating: Optional[float]
    type: str
    created: datetime
    modified: datetime


@dataclass(slots=True)
class GenreFilmWork:
    genre_id: UUID
    film_work_id: UUID
    created: datetime


@dataclass(slots=True)
class PersonFilmWork:
    person_id: UUID
    film_work_id: UUID
    role: str
    created: datetime

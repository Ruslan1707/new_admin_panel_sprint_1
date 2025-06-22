import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# ── МИКСИНЫ ─────
class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


# ── ОСНОВНЫЕ МОДЕЛИ ─────
class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'
        indexes = [
            models.Index(fields=['full_name'], name='person_full_name_idx'),
        ]

    def __str__(self) -> str:
        return self.full_name


class PersonFilmWork(UUIDMixin):

    class RoleType(models.TextChoices):
        ACTOR = 'actor', 'Actor'
        PRODUCER = 'producer', 'Producer'
        DIRECTOR = 'director', 'Director'

    film_work = models.ForeignKey(
        'FilmWork',
        on_delete=models.CASCADE,
        db_index=True,
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        db_index=True,
    )
    role = models.CharField('role', max_length=8, choices=RoleType.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = 'Участие персоны'
        verbose_name_plural = 'Участия персон'
        constraints = [
            models.UniqueConstraint(
                fields=('film_work', 'person', 'role'),
                name='person_film_work_uniq',
            ),
        ]


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):

    class FilmType(models.TextChoices):
        MOVIE = "movie", "Movie"
        TV_SHOW = "tv_show", "TV Show"

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation date"), blank=True, null=True)
    rating = models.FloatField(
        "rating",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(_("type"), max_length=7, choices=FilmType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"
        indexes = [
            models.Index(fields=["creation_date"], name="film_creation_date_idx"),
            models.Index(fields=["rating"], name="film_rating_idx"),
            models.Index(fields=["type"], name="film_type_idx"),
        ]

    def __str__(self) -> str:
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        db_table = "content\".\"genre_film_work"

"""
Data models, validators, and ETL tools for scraped media data.

Includes support for film reviews (via IMDb), music albums (via Spotify),
and related information (via Wikipedia).

Highlights
----------

.. currentmodule:: datopy.models.media

.. rubric:: Data models

.. autosummary::
    :nosignatures:

    IMDbFilm
    SpotifyAlbum

Complete API
------------
"""

import re
import typing
import doctest
import pandas as pd
from typing import (
    List,
    Tuple,
    TypeVar,
    Literal,
    NamedTuple,
)
from pydantic import (
    Field,
    BaseModel,
    TypeAdapter,
    ValidationInfo,
    ValidationError,
    field_validator,
)
from typing_extensions import Annotated

import imdb
import spotipy
import wptools
from imdb import Cinemagoer
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials

# import datopy._settings
from datopy.etl import omit_string_patterns
from datopy.workflow import doctest_function
from datopy.modeling import BaseProcessor, CustomTypes


# --------------------------
# --- Metadata retrieval ---
# --------------------------

# Custom type containing search terms with required 'title' attribute
# TODO archive this: does not generalize well
# class MediaSearchTerms(NamedTuple):
#     title: str
#     creator: str | None = None

# Film = NamedTuple('Film', [('title', str), ('artist', None)])
# Album = NamedTuple('Album', [('title', str), ('artist', str)])
# Book = NamedTuple('Book', [('title', str), ('artist', str | None)])


class MediaQuery(NamedTuple):
    """
    Query object types for media metadata retrieval.

    .. todo:: test

    """
    title: str
    artist: str | None = None


Film = type('Film', (MediaQuery,), {})
Album = type('Album', (MediaQuery,), {})
Book = type('Book', (MediaQuery,), {})


# class MediaQuery:
#     """Query object types for media metadata retrieval."""
#     Film = Film
#     Album = Album
#     Book = Book


class IMDbFilm(BaseModel):
    r"""
    Data model for processed imdb metadata.

    Examples
    --------
    >>> from pydantic import ValidationError
    >>> from datopy.models.media import IMDbFilm
    >>> from datopy._examples import imdb_film_retrieve

    Valid film

    >>> valid_film = IMDbFilm(
    ...     title='name 10!', imdb_id='tt1234567', kind='movie',
    ...     year=1990, rating=7.2, votes=122,
    ...     genres='romantic comedy, thriller', cast='mrs smith,mr smith',
    ...     plot='alas! once upon a time, ...',
    ...     budget_mil=1123929)

    Invalid film

    >>> invalid_film = dict(
    ...     title='name', imdb_id='tt12', year=1975, votes=-2, rating=5.0)
    >>> try:
    ...     IMDbFilm(**invalid_film)
    ... except ValidationError as e:
    ...     print(e)          # use pprint.pp(e.errors()) for easy-to-read list
    3 validation errors for IMDbFilm
    imdb_id
      String should match pattern '^tt.*\d{7}$' [type=string_pattern_mismatch, input_value='tt12', input_type=str]
        For further information visit https://errors.pydantic.dev/2.7/v/string_pattern_mismatch
    kind
      Field required [type=missing, input_value={'title': 'name', 'imdb_i...tes': -2, 'rating': 5.0}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.7/v/missing
    votes
      Input should be greater than or equal to 0 [type=greater_than_equal, input_value=-2, input_type=int]
        For further information visit https://errors.pydantic.dev/2.7/v/greater_than_equal

    Survey available fields and types

    >>> import pprint
    >>> from datopy.models.media import Film
    >>> from datopy._examples import imdb_film_retrieve
    >>> from datopy.modeling import apply_recursive
    >>> film = imdb_film_retrieve(Film('spirited away'))

    ..
        # >>> film.keys()
        # >>> pprint.pp(apply_recursive(lambda x: type(x).__name__, film), depth=3)

    """

    # Identifiers
    title: CustomTypes.CSVnumstr
    imdb_id: str = Field(
        pattern=r'^tt.*\d{7}$',
        description="Unique 7-digit IMDb tt identifier"
    )
    kind: CustomTypes.CSVnumstr = Field(
        examples=['movie', 'tv series'],
        description="Retrieved from: `type`"
    )

    # Numeric
    year: int = Field(ge=1880, le=3000)
    rating: float = Field(ge=0, le=10)
    votes: int = Field(ge=0)
    runtime_mins: float | None = Field(gt=0, default=None)

    # String lists
    genres: CustomTypes.CSVstr | None = Field(default=None)
    countries: CustomTypes.CSVstr | None = Field(default=None)
    director: CustomTypes.CSVstr | None = Field(default=None)
    writer: CustomTypes.CSVstr | None = Field(default=None)
    composer: CustomTypes.CSVstr | None = Field(default=None)
    cast: CustomTypes.CSVstr | None = Field(default=None)

    # Strings
    plot: CustomTypes.CSVnumsent | None = Field(default=None)
    synopsis: CustomTypes.CSVnumsent | None = Field(default=None)
    plot_outline: CustomTypes.CSVnumsent | None = Field(default=None)

    # Financial
    budget_mil: float | None = Field(
        ge=0,
        default=None,
        description="Strip $/, & text after first space"
    )
    opening_weekend_gross_mil: float | None = Field(ge=0, default=None)
    cumulative_worldwide_gross_mil: float | None = Field(ge=0, default=None)

    @field_validator('imdb_id', 'kind')
    @classmethod
    def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            # info.field_name is the name of the field being validated
            is_alphanumeric = v.replace(' ', '').isalnum()
            assert is_alphanumeric, f'{info.field_name} must be alphanumeric'
        # return v.title()
        return v


# TODO place media/animals/nations models/queries/processors in
# {media/eco/global}_pulse.py
# TODO implement 4 pydantic processed data models + 1 valid/invalid demo

class SpotifyAlbum(BaseModel):
    """
    Data model for processed Spotify metadata.

    Raw data schema reference: 'datopy/output/spotify_album_schema.json'.
    """
    # fields of interest:

    title: str
    album_type: str


class WikiBook(BaseModel):
    """
    Data model for processed Wikipedia novel metadata.

    Raw data schema reference: 'output/wiki_book_schema.json'.
    """
    # fields of interest:

    title: str


class WikiFilm(BaseModel):
    """
    Data model for processed Wikipedia film metadata.

    Raw data schema reference: 'datopy/output/wiki_film_schema.json'.
    """
    # fields of interest:

    title: str


class WikiAlbum(BaseModel):
    """
    Data model for processed Wikipedia album metadata.

    Raw data schema reference: 'datopy/output/wiki_album_schema.json'.
    """
    # fields of interest:

    title: str


# XXX Scratch tests
# valid_obj = {}
# invalid_obj = {}
# pd.DataFrame(pd.json_normalize(dict(valid_obj)))
# pd.DataFrame(pd.json_normalize(dict(invalid_obj)))

# try: IMDbFilm(**valid_obj)
# except ValidationError as e: pprint.pp(e.errors())
# try: IMDbFilm(**invalid_obj)
# except ValidationError as e: pprint.pp(e.errors())


# --------------------------
# --- Metadata retrieval ---
# --------------------------

# Subclass Processor

# TODO move these to media
# TODO implement 5 subclasses

class IMDbFilmProcessor(BaseProcessor):
    """
    _summary_.
    """
    def retrieve(self):
        # title = self.query.title

        # Retrieval routine

        obj = []
        self.obj = obj
        return self

    def process(self):
        # Processing routine

        data = []
        self.data = data
        return self


# XXX Scratch tests
# IMDbFilm = []; Film = []
# film = IMDbFilmProcessor(model=IMDbFilm, query=Film)
# film.retrieve().process().to_df()


if __name__ == "__main__":
    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod(verbose=True)
    # doctest_function(IMDbFilm, globs=globals(), verbose=False)

    ## One-off tests
    pass

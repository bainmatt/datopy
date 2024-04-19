"""
The :mod:`models` includes examples of data models/validators and related ETL
routines for media datasets, ecological datasets, and global datasets.
"""

from .media_pulse import (
    IMDbFilm,
    Album,
    Film,
    Book,
    # BaseProcessor,
    IMDbFilmProcessor,
    SpotifyAlbum,
    WikiAlbum,
    WikiBook,
    WikiFilm,
    MediaQuery,
    # CustomTypes,
)

__all__ = [
    "IMDbFilm",
    "Album",
    "Film",
    "Book",
    "BaseProcessor",
    "IMDbFilmProcessor",
    "SpotifyAlbum",
    "WikiAlbum",
    "WikiBook",
    "WikiFilm",
    "MediaQuery",
    "CustomTypes",
]

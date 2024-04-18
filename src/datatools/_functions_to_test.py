"""
Some boilerplate functions for demonstrating the pytest testing framework.
Corresponding test module: 'tests/test__functions_to_test.py'.
Reference: https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject?tab=readme-ov-file
"""

import re
import enum
import pandas as pd
from imdb import Cinemagoer

from datatools.display_dataset import make_df


# --- Interfaces ---
class LikeState(enum.Enum):
    empty = enum.auto()
    liked = enum.auto()
    disliked = enum.auto()


click_like_transitions = {
    LikeState.empty: LikeState.liked,
    LikeState.liked: LikeState.empty,
    LikeState.disliked: LikeState.liked,
}

click_dislike_transitions = {
    LikeState.empty: LikeState.disliked,
    LikeState.liked: LikeState.disliked,
    LikeState.disliked: LikeState.empty,
}


def click_like(s: LikeState) -> LikeState:
    return click_like_transitions[s]


def click_dislike(s: LikeState) -> LikeState:
    return click_dislike_transitions[s]


def click_many(s: LikeState, clicks: str) -> LikeState:
    for c in clicks:
        c = c.lower()
        if c == 'l':
            s = click_like(s)
        elif c == 'd':
            s = click_dislike(s)
        else:
            raise ValueError('invalid click')
    return s


# --- String patterns ---
def omit_string_patterns(input_string: str, patterns: list[str]) -> str:
    """Helper to prune multiple character patterns from a string at once."""
    pattern = '|'.join(re.escape(p) for p in patterns)
    return re.sub(pattern, '', input_string)


# --- API-based data retrieval ---
def imdb_film_retrieve(movie_title: str) -> object:
    """IMDb film metadata retrieval routine.
    """
    ia = Cinemagoer()
    movies = ia.search_movie(movie_title)

    if not movies:
        raise LookupError(f"No result found for {movie_title}.")
    else:
        obj = ia.get_movie(movies[0].movieID)

    return obj


# --- Requiring local depdencies / globa variables ---
def transpose_table(cols: list[int], ind: list[int]) -> pd.DataFrame:
    df = make_df(ind, cols)
    return df

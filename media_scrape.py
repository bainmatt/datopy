""" 
Tools for organized, efficient scraping of metadata for movies and movie reviews (via IMDb), music albums (via Spotify), and general topics (via Wikipedia).
"""

import re
import requests
import doctest
import pprint
import json
import pandas as pd
from typing import List
from datetime import datetime
from jsonschema import validate
from dataclasses import dataclass, asdict
from pydantic import BaseModel, ValidationError, PositiveInt

import wptools
import spotipy
import imdb
from spotipy.oauth2 import SpotifyClientCredentials
from imdb import Cinemagoer
from bs4 import BeautifulSoup

from display_dataset import display

# -------------------------------
# --- Data validation schemas ---
# -------------------------------

# XXX auto-schema generation tests
# https://domsignal.com/json-schema-generator
# ia = Cinemagoer()
# movies = ia.search_movie('Crouching tiger hidden dragon')
# example_imdb_object = ia.get_movie(movies[0].movieID)
# example_wiki_object = wptools.page("Canada").get_parse().data['infobox']

# def get_schema(obj):
#     schema = {}
#     for field, value in obj.items():
#         if not(isinstance(value, (list, dict))):
#             schema[field] = (type(value))
#             continue
#         else:
#             schema[field] = {}
            
#             for index, subfield in enumerate(value): 
#                 schema[field][index] = type(subfield)
#                 if not(isinstance(subfield, (list, dict, imdb.Person.Person))):
#                     continue
#                 else:
#                     schema[field][index] = {}
                    
#                 for tertiary_field, tertiary_value in subfield.items():
#                     schema[field][index][tertiary_field] = type(tertiary_field)
                    
#     return schema

# movie_schema = get_schema(example_imdb_object)
# wiki_schema = get_schema(example_wiki_object)
# pprint.pp(movie_schema)
# pprint.pp(wiki_schema)

# XXX Data validation tests
# NOTE Opt for manually defined schemas for retrieved data. Data
# is messy and unpredictable and every automated attempt will either screw up 
# edge cases or overlook nuances/quirks (Ex: an integer dressed up as a string,
# masquerading as an iterable).


# XXX Raw data
MOVIE_SCHEMA = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

# -----------------------------------------------------------------------------
# TODO load a few test json objects
valid_raw_movie = {"name" : "Eggs", "price" : 34.99}
invalid_raw_movie = {"name" : 1, "price" : 34.99}

validate(instance=valid_raw_movie, schema=MOVIE_SCHEMA)
# validate(instance=invalid_raw_movie, schema=MOVIE_SCHEMA)
# -----------------------------------------------------------------------------

# XXX Processed data
class Movie(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]

# -----------------------------------------------------------------------------
valid_processed_movie = {
    'id': 1, 'tastes': dict(a=3), 
    'signup_ts': datetime(1990, 4, 1)
} 
invalid_processed_movie = {
    'id': 'not an int', 'tastes': {'hek'},
    'signup_ts': datetime(1990, 4, 1)
}  
valid_processed_movie_instance = Movie(**valid_processed_movie)  
# invalid_processed_movie_instance = Movie(**invalid_processed_movie)  
pd.DataFrame(pd.json_normalize(dict(valid_processed_movie_instance)))
# pd.DataFrame(pd.json_normalize(dict(invalid_processed_movie_instance)))

try:
    Movie(**valid_processed_movie)  
except ValidationError as e:
    pprint.pp(e.errors())
# try:
#     Movie(**invalid_processed_movie)  
# except ValidationError as e:
#     pprint.pp(e.errors())
# -----------------------------------------------------------------------------

# XXX BaseProcessor
class BaseProcessor:
    def __init__(self, **args):
        self.args = args
        
    def retrieve(self, x: list):
        return sum(x)

    def process(self):
        raise NotImplementedError

# XXX Subclass Processor
class MovieProcessor(BaseProcessor):
    def process(self, y: list):
        return sum(y)*5

# -----------------------------------------------------------------------------
MovieProcessor().retrieve([4,5,6])
MovieProcessor().process([4,5,6])
# -----------------------------------------------------------------------------

# TODO discard this
# @dataclass
# class Movie:
#     name: str
#     age: int
    
# valid_processed_movie = Movie(name='mark', age=21)
# invalid_processed_movie = Movie(name=21, age=21)
# pd.DataFrame(pd.json_normalize(asdict(valid_processed_movie)))
# pd.DataFrame(pd.json_normalize(asdict(invalid_processed_movie)))

# -----------------
# --- Wikipedia ---
# -----------------
### Get Wiki 
# (wiki_extract_film_metadata, wiki_extract_novel_metadata, wiki_extract_album_metadata)

# XXX wiki scratch
# page = "Canada"
# wiki_info = wptools.page(page).get_parse().data['infobox']
# pprint.pp(wiki_info)
# wiki_info['currency']


### Get lists
# TODO wrap in function (take first and last entry (relative indices non-0'ed))
# Find listing_page here: https://en.wikipedia.org/wiki/List_of_lists_of_lists
listing_page = "List of legendary creatures from China"
wiki_parse = wptools.page(listing_page).get_parse().data['parsetree']

regex_pattern = re.compile("\[\[(.*?)\]\]")
matches = regex_pattern.findall(wiki_parse)
pages = [match.split('|')[0].strip() for match in matches]
target_pages = pages[4:-3]
pprint.pp(target_pages)

# Test 
# TODO skip broken links (e.g., Dennis the Menace (1987))
# wiki_info = []
# for index, page in enumerate(target_pages):
#     print(page)
#     wiki_info.append(wptools.page(page).get_parse().data['infobox'])
# pprint.pp(wiki_info)

# ---------------
# --- Spotify ---
# ---------------
### Get Spotify

# ------------
# --- IMdB ---
# ------------

### Get IMdB

def get_imdb_id(movie_title: str) -> str:
    """
    Retrieves the unique IMDb identifier associated with a film or tv show.

    Parameters
    ----------
    movie_title : str
        Title of film or tv show (sensitive to spelling but not case).

    Returns
    -------
    imdb_id : str
        The unique IMDb tt identifier associated with the show.
        
    Examples
    --------
    >>> movie_title = "the shawshank redemption"
    >>> tt_id = get_imdb_id(movie_title)
    >>> tt_id
    'tt0111161'

    >>> movie_title = "ths shukshank redumption"
    >>> tt_id = get_imdb_id(movie_title)
    >>> tt_id
    "No IMDb Identifier found for 'ths shukshank redumption'."
    """
    
    base_url = "https://www.imdb.com"
    search_url = f"{base_url}/find?q={movie_title}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        search_response = requests.get(search_url, headers=headers)
        search_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    
    soup = BeautifulSoup(search_response.content, 'html.parser')
    result_links = soup.find_all('a', href=True)

    for link in result_links:
        # Return first link containing ttid
        if '/title/tt' in link['href']:
            imdb_id = link['href'].split('/title/')[1].split('/')[0]
            return imdb_id

    # If no links contain ttid
    return f"No IMDb Identifier found for '{movie_title}'."

def get_imdb_reviews(movie_id: str, num_reviews: int = 5) -> List[str]:
    r"""
    _summary_

    Parameters
    ----------
    movie_id : str
        The unique IMDb tt identifier supplied by `get_imdb_id`.
    num_reviews : int, default=5
        Number of reviews to retrieve.

    Returns
    -------
    reviews : List[str]
        _description_
        
    Examples
    --------
    >>> movie_title = "finding nemo"
    >>> movie_id = get_imdb_id(movie_title)
    >>> movie_reviews = get_imdb_reviews(movie_id, num_reviews=2)
    >>> for i, review in enumerate(movie_reviews, start=1):
    ...     print(f"Review {i}:\n{textwrap.fill(review[:50], 79)} ... \n");
    Review 1:
    I'll be totally honest and confirm to you that eve ... 
    <BLANKLINE>
    Review 2:
    I have enjoyed most of the computer-animated films ... 
    <BLANKLINE>
    """
    
    base_url = f"https://www.imdb.com/title/{movie_id}/reviews"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        review_containers = soup.find_all('div', 
                                          class_='text show-more__control')

        reviews = []
        for review_container in review_containers[:num_reviews]:
            review_text = review_container.text.strip()
            reviews.append(review_text)

        return reviews
    else:
        print(f"Failed to retrieve reviews. Status code: {response.status_code}")
        return None


def get_film_metadata(movie_title: str) -> pd.DataFrame:
    r"""
    _summary_

    Parameters
    ----------
    movie_title : str
        Title of a film or tv show (sensitive to spelling but not case).

    Returns
    -------
    film_df : pd.DataFrame
        _description_
        
    Examples
    --------
    >>> title = 'donnie darko'
    >>> film_df = get_film_metadata(title)
    >>> film_df.T[0]
    title                                                 Donnie Darko
    imdbID                                                     0246578
    type                                                         movie
    year                                                          2001
    genres                            Drama, Mystery, Sci-Fi, Thriller
    writers                                              Richard Kelly
    countries                                            United States
    runtime (min)                                                  113
    directors                                            Richard Kelly
    composer                                           Michael Andrews
    cast             Jake Gyllenhaal, Holmes Osborne, Maggie Gyllen...
    rating                                                         8.0
    Votes                                                       847582
    Plot Outline     Donnie Darko doesn't get along too well with h...
    Plot             After narrowly escaping a bizarre accident, a ...
    Synopsis         Donnie Darko (Jake Gyllenhall) is a troubled t...
    Name: 0, dtype: object
    """
    
    movie_fields = ['title', 'imdbID', 'kind', 'year', 'runtime',
                    'genres', 'countries', 'directors', 'writers', 
                    'composers', 'cast', 'rating', 'votes', 
                    'plot outline', 'plot', 'synopsis']
    
    # Create an IMDb object
    ia = Cinemagoer()

    # Search for the movie by title
    movies = ia.search_movie(movie_title)

    if movies:
        # Get the first movie (assumed to be the correct one)
        movie = ia.get_movie(movies[0].movieID)

        # Extract movie attributes
        # TODO Identify and consider generalizability of extraction patterns
        movie_data = {
            "title": movie.get('title', None),
            "imdbID": movie.get('imdbID', None),
            "type": movie.get('kind', None),
            "year": movie.get('year', None),
            "runtime (min)": movie.get('runtime')[0],
            "rating": movie.get('rating', None),
            "votes": movie.get('votes', None),
            "genres": ', '.join(movie.get('genres', None)),
            "countries": ', '.join(movie.get('countries', None)),
            "director": (
                movie['director'][0].get('name', None) 
                if 'director' in movie else None
            ),
            "writer": (
                movie['writer'][0].get('name', None)
                if 'writer' in movie else None
            ),
            "composer": (
                movie['composer'][0].get('name', None)
                if 'composer' in movie else None
            ),
            "cast": ', '.join(
                actor.get('name', None)
                for actor in movie['cast'] if 'cast' in movie
            ),
            "plot": (
                movie['plot'][0] if 'plot' in movie else None
            ),
            "synopsis": (
                movie['synopsis'][0] if 'synopsis' in movie else None
            ),
            "plot outline": movie.get('plot outline', None),
        }
        
        # Create a DataFrame
        film_df = pd.DataFrame([movie_data])    
        return film_df
    else:
        print(f"{movie_title} not found.")
        film_df = pd.DataFrame(
            [{movie_field: None for movie_field in movie_fields}]
        )   
        return film_df
    

if __name__ == "__main__":    
    # Comment out (2) to run all tests in script; (1) to run specific tests
    # doctest.testmod(verbose=True)
    # doctest_function(get_film_metadata, globs=globals())
    
    ## One-off tests
    title = 'attack on titan'
    # film_df = get_film_metadata(title)
    # display("film_df.T[0]").r(globals())
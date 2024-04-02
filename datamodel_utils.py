""" 
Tools for data retrieval and entry, from generating data models to processing raw data and populating missing metadata fields. 

# --- Data model considerations ---

"""

import re
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

import settings
from display_dataset import display

# ----------------------------------
# --- Data dictionary generation ---
# ----------------------------------

# XXX Automatic data dictionary generation
def _list_to_dict(obj: list) -> dict:
    """
    Provide a dictionary representation of a list or other non-dictionary or string-like iterable, using indices as keys. 
    
    Example
    -------
    >>> my_list = [1, 'two', [3], {'four': 5}]
    >>> _list_to_dict(my_list)
    {1: 1, 2: 'two', 3: [3], 4: {'four': 5}}
    """
    return {(key + 1): value for key, value in enumerate(obj)}

def iterable_to_schema(obj, special_types: tuple = (dict,)) -> dict:
    """
    _summary_

    Parameters
    ----------
    obj : _type_
        _description_
    special_types: tuple
        _description_

    Returns
    -------
    dict: 
        _description_
    """
        
    if isinstance(obj, special_types):
        return {key: iterable_to_schema(value, special_types) 
                for key, value in obj.items()}
    
    elif isinstance(obj, (list, tuple, set)):
        return {key: iterable_to_schema(value, special_types) 
                for key, value in _list_to_dict(obj).items()}
    
    elif isinstance(obj, type):
        return obj.__name__
    elif isinstance(obj, str):
        return type(obj).__name__
    else:
        return type(obj).__name__
    
    
# ------------------------------
# --- Data validation scheme ---
# ------------------------------

    
# TODO generate pydantic data model from schema 
# (+ use JSON as intermediary & save a few examples per resource to file)
# TODO write corresponding tests for schema generator


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


# ----------------------------------
# --- Data processing base class ---
# ----------------------------------

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

# --------------------------
# --- Metadata retrieval ---
# --------------------------


# -----------------------
# --- Topic retrieval ---
# -----------------------

### Get lists
# TODO wrap in function (take first and last entry (relative indices non-0'ed))
# Find listing_page here: https://en.wikipedia.org/wiki/List_of_lists_of_lists
listing_page = "List of legendary creatures from China"
wiki_parse = wptools.page(listing_page).get_parse().data['parsetree']

regex_pattern = re.compile("\[\[(.*?)\]\]")
matches = regex_pattern.findall(wiki_parse)
pages = [match.split('|')[0].strip() for match in matches]
target_pages = pages[4:-3]
# pprint.pp(target_pages)



if __name__ == "__main__":    
    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod(verbose=True)
    # doctest_function(get_film_metadata, globs=globals())
        
    ## One-off tests
    # XXX Data dictionary stuff
    special_types = (
        dict, imdb.Person.Person, imdb.Movie.Movie, imdb.Company.Company
    )
    
    # Movie
    # ia = Cinemagoer()
    # movies = ia.search_movie('castlevania')
    # my_imdb_obj = ia.get_movie(movies[0].movieID)
    # schema = iterable_to_schema(my_imdb_obj, special_types)
    
    # Album
    # sp = spotipy.Spotify(
    #     client_credentials_manager=SpotifyClientCredentials()
    # )
    # results = sp.search(
    #     q=f'artist:{"radiohead"} album:{"kid A"}', type='album'
    # )
    # my_spotify_obj = results['albums']['items'][0]
    # schema = iterable_to_schema(my_spotify_obj, special_types)
    
    # Wikipedia
    # my_wiki_obj = wptools.page("Canada").get_parse().data['infobox']
    # schema = iterable_to_schema(my_wiki_obj, special_types)
    
    # pprint.pp(schema, depth=3)
    # pprint.pp(pd.json_normalize(schema).T[0], compact=True)
    
    # XXX Data model and validation stuff
    # Movie(**schema)  
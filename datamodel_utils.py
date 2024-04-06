""" 
Tools for data retrieval and entry, from generating data models to processing raw data and populating missing metadata fields. 
"""

import re
import doctest
import pprint
import json
import pandas as pd

from typing import List, Tuple
from datetime import datetime
from collections.abc import Iterable
from jsonschema import validate
from dataclasses import dataclass, asdict
from pydantic import BaseModel, ValidationError, PositiveInt

import pydantic
import wptools
import spotipy
import imdb

from spotipy.oauth2 import SpotifyClientCredentials
from imdb import Cinemagoer
from bs4 import BeautifulSoup

import _settings

from display_dataset import display
from nb_utils import doctest_function


# ----------------------------------
# --- Data dictionary generation ---
# ----------------------------------

def _list_to_dict(obj: list, max_items: int = None) -> dict:
    """
    Provide a dictionary representation of a list or other non-dictionary or string-like iterable, using indices as keys. 
    
    Parameters
    ----------
    obj : list
        A list to convert to a dictionary representation.
    max_items : int, default=None
        Option to impose a limit on the number of elements to iterate over.
        Intended use: constructing pattern-based data models from a sample.
    
    Returns
    dict : The supplied list's dictionary representation.
    -------
    
    Examples
    --------
    >>> my_list = [1, 'two', [3], {'four': 5}]
    >>> _list_to_dict(my_list)
    {1: 1, 2: 'two', 3: [3], 4: {'four': 5}}
    
    >>> my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> _list_to_dict(my_list, max_items=5)
    {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    
    >>> my_dict = dict(a=1, b='two')
    >>> _list_to_dict(my_dict)
    Not running conversion since obj is already a dictionary.
    {'a': 1, 'b': 'two'}
    """
    if isinstance(obj, dict): 
        print("Not running conversion since obj is already a dictionary.")
        return obj
    else:
        return {(key + 1): value for key, value in enumerate(obj)
                if (max_items is None) or (key < max_items)}
        

def _compare_dict_keys(dict1: dict, dict2: dict) -> dict:   
    """
    Recursively compare two dictionaries and identify missing keys.
    
    Parameters
    ----------
    dict1 : dict
        The reference dictionary.
    dict2 : dict
        The comparison dictionary to be checked against `dict1`.

    Returns
    -------
    result : dict
        The nested dictionary of fields missing from `dict2` relative `dict1`.
        
    Examples
    --------
    Setup
    >>> import copy
    >>> dict1 = {'a1': 1, 'a2': 'two', 'a3': [3],
    ...          'b1': {'b11': 1, 'b12': 'two', 'b13': [3]},
    ...          'c1': {'c11': {'c111': 1, 'c112': 'two', 'c113': [3]}}
    ... }

    Identical dictionaries
    >>> dict2 = copy.deepcopy(dict1)
    >>> _compare_dict_keys(dict1, dict2)

    Missing nesting level 0 key
    >>> del dict2['a1']
    >>> _compare_dict_keys(dict1, dict2)
    {'missing_keys': ['a1']}

    Missing nesting level 1 key
    >>> dict2 = copy.deepcopy(dict1)
    >>> del dict2['b1']['b12']
    >>> _compare_dict_keys(dict1, dict2)
    {'nested_diff': {'b1': {'missing_keys': ['b12']}}}
    
    Missing nesting level 2 key
    >>> dict2 = copy.deepcopy(dict1)
    >>> del dict2['c1']['c11']['c113']
    >>> _compare_dict_keys(dict1, dict2)
    {'nested_diff': {'c1': {'nested_diff': {'c11': {'missing_keys': ['c113']}}}}}
    """
    
    if isinstance(dict1, dict) and not isinstance(dict2, dict):
        return 'missing nested dictionary'

    if not (isinstance(dict1, dict) and isinstance(dict2, dict)):
        return None
    
    missing_keys = set(dict1.keys()) - set(dict2.keys())
    shared_keys = set(dict1.keys()).intersection(set(dict2.keys()))
    
    # Initialize difference dictionary
    diff_dict = {}
    for key in shared_keys:
        nested_diff = _compare_dict_keys(dict1[key], dict2[key])
        # Add any differences to the difference
        if nested_diff is not None:
            diff_dict[key] = nested_diff
    
    # Return result if no missing keys or no diffs in nested dicts found
    if missing_keys or diff_dict:
        result = {}
        if missing_keys:
            result['missing_keys'] = list(missing_keys)
        if diff_dict:
            result['nested_diff'] = diff_dict
        return result

    # Return None if no missing keys or differences found
    return None


def _omit_patterns(input_string: str, patterns: List[str]) -> str:
    r"""
    Helper to prune multiple character patterns from a string at once.

    Parameters
    ----------
    input_string : str
        The to-be-cleaned string. 
    patterns : List[str] 
        A list of patterns to omit from the string.

    Returns
    -------
    str : The input string with the supplied patterns ommitted.
        
    Examples
    --------
    >>> input_string = "[[A \\\\ messy * string * with undesirable /patterns]]"
    >>> print(input_string)
    [[A \\ messy * string * with undesirable /patterns]]
    >>> patterns_to_omit = ["[[", "]]", "* ", "\\\\ ", "/", "messy ", "un" ]
    >>> output_string = _omit_patterns(input_string, patterns_to_omit)
    >>> print(output_string)
    A string with desirable patterns
    """
    pattern = '|'.join(re.escape(p) for p in patterns)
    return re.sub(pattern, '', input_string)


def serialize_scraped_data(obj, max_items: int = None) -> dict:
    """
    Coerce unique dataclasses from scraped objects into serializable format.
        
    Parameters
    ----------
    obj : _type_
        _description_
    max_items : int, default=None
        _description_
        
    Returns
    -------
    dict: 
        _description_
    """
    # Handle dictionary-like objects
    if hasattr(obj, 'items'):
        return {key: serialize_scraped_data(value, max_items) 
                for key, value in obj.items()}
            
    # Handle list-like objects
    elif isinstance(obj, (list, tuple, set)):
        return {key: serialize_scraped_data(value, max_items) 
                for key, value in _list_to_dict(obj, max_items).items()}
            
    # Handle base cases
    elif isinstance(obj, str):
        return str(obj)
    else:
        return str(obj)


def iterable_to_schema(obj, max_items: int = None) -> dict:
    """
    _summary_

    Parameters
    ----------
    obj : _type_
        _description_
    max_items : int, default=None
        _description_
    Returns
    -------
    dict: 
        _description_
    """
    # Handle dictionary-like objects
    if hasattr(obj, 'items'):
        return {key: iterable_to_schema(value, max_items) 
                for key, value in obj.items()}
    
    # Handle list-like objects
    elif isinstance(obj, (list, tuple, set)):
        return {key: iterable_to_schema(value, max_items) 
                for key, value in _list_to_dict(obj, max_items).items()}
    
    # Handle base cases
    # TODO omit this! indicates base case already reached
    elif isinstance(obj, type):
        return obj.__name__
    elif isinstance(obj, str):
        return type(obj).__name__
    else:
        return type(obj).__name__

    
# ------------------------------
# --- Data validation scheme ---
# ------------------------------

# --- Data model considerations ---
# - Fields: descriptions, required entries
# - Type-specific: num (range), str (regex), cat (options)
# - List-like container types: uniformity of elements, length, options, order

# NOTE Generally opt for manually defined schemas for retrieved data. Data
# is messy and unpredictable and every automated attempt will either screw up 
# edge cases or overlook nuances/quirks (Ex: an integer dressed up as a string,
# masquerading as an iterable).
    
# TODO implement JSON schema for 5 scraped objects
# TODO implement corresponding pydantic data model for processed objects
# TODO valid + invalid ex of each (5*2 * 2) & validate w/ JSON/pydantic resp

# TODO probably move these examples/validation tests to _examples.py

# Raw API-retrieved data schemas and JSON data validation
with open('models/imdb_model.json') as file:
    MOVIE_SCHEMA = json.load(file)

valid_raw_movie = {
    "title": "green eggs and ham", "year": 1904, "kind": "movie", 
    "director": {"1": {"name": "Jill Smith"}}
}
# invalid_raw_movie = {"name": 1, "price": 34.99}

validate(instance=valid_raw_movie, schema=MOVIE_SCHEMA)
# validate(instance=invalid_raw_movie, schema=MOVIE_SCHEMA)

# -----------------------------------------------------------------------------
# XXX (rough pydantic validation tests)
# Processed data model
class Movie(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]

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

# BaseProcessor

# TODO implement BaseProcessor

class BaseProcessor:
    def __init__(self, **args):
        self.args = args
        
    def retrieve(self, x: list):
        return sum(x)

    def process(self):
        raise NotImplementedError


# --------------------------
# --- Metadata retrieval ---
# --------------------------

# Subclass Processor

# TODO implement 5 subclasses



# -----------------------------------------------------------------------------
# XXX (rough tests)
class MovieProcessor(BaseProcessor):
    def process(self, y: list):
        return sum(y)*5

MovieProcessor().retrieve([4,5,6])
MovieProcessor().process([4,5,6])
# -----------------------------------------------------------------------------

# -----------------------
# --- Topic retrieval ---
# -----------------------

# TODO take first and last entry (relative indices non-0'ed))

def retrieve_wiki_topics(listing_page: str, verbose: bool = True) -> List[str]:
    """
    _summary_
    
    Find listing_page here: https://en.wikipedia.org/wiki/List_of_lists_of_lists

    Parameters
    ----------
    listing_page : str
        _description_
    verbose : bool, default=True
        _description_ 

    Returns
    -------
    target_pages : List[str]
        _description_
    """
    
    wiki_parse = wptools.page(listing_page).get_parse().data['parsetree']

    regex_pattern = re.compile("\[\[(.*?)\]\]")
    matches = regex_pattern.findall(wiki_parse)
    pages = [match.split('|')[0].strip() for match in matches]
    target_pages = pages[4:-3]
    
    if verbose:
        pprint.pp(target_pages)
    
    return target_pages

# listing_page = "List of legendary creatures from China"
# retrieve_wiki_topics(listing_page)


if __name__ == "__main__":    
    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod(verbose=False)
    # doctest_function(get_film_metadata, globs=globals())
        
    ## One-off tests
    
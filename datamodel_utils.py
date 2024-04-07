""" 
Tools for data retrieval and entry, from generating data models to processing raw data and populating missing metadata fields. 
"""

import re
import doctest
import pprint
import json
import pandas as pd

from typing import List, Tuple, Any, Callable
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

from display_dataset import eva
from nb_utils import doctest_function


# ----------------------------------
# --- Data dictionary generation ---
# ----------------------------------

def list_to_dict(obj: list, max_items: int = None) -> dict:
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
    >>> list_to_dict(my_list)
    {1: 1, 2: 'two', 3: [3], 4: {'four': 5}}
    
    >>> my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> list_to_dict(my_list, max_items=5)
    {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    
    >>> my_dict = dict(a=1, b='two')
    >>> list_to_dict(my_dict)
    Not running conversion since obj is already a dictionary.
    {'a': 1, 'b': 'two'}
    """
    if isinstance(obj, dict): 
        print("Not running conversion since obj is already a dictionary.")
        return obj
    else:
        return {(key + 1): value for key, value in enumerate(obj)
                if (max_items is None) or (key < max_items)}
        

def compare_dict_keys(dict1: dict, dict2: dict) -> dict:   
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
    >>> compare_dict_keys(dict1, dict2)

    Missing nesting level 0 key
    >>> del dict2['a1']
    >>> compare_dict_keys(dict1, dict2)
    {'missing_keys': ['a1']}

    Missing nesting level 1 key
    >>> dict2 = copy.deepcopy(dict1)
    >>> del dict2['b1']['b12']
    >>> compare_dict_keys(dict1, dict2)
    {'nested_diff': {'b1': {'missing_keys': ['b12']}}}
    
    Missing nesting level 2 key
    >>> dict2 = copy.deepcopy(dict1)
    >>> del dict2['c1']['c11']['c113']
    >>> compare_dict_keys(dict1, dict2)
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
        nested_diff = compare_dict_keys(dict1[key], dict2[key])
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


def omit_string_patterns(input_string: str, patterns: List[str]) -> str:
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
    >>> output_string = omit_string_patterns(input_string, patterns_to_omit)
    >>> print(output_string)
    A string with desirable patterns
    """
    pattern = '|'.join(re.escape(p) for p in patterns)
    return re.sub(pattern, '', input_string)

    
def apply_recursive(func: Callable[..., Any], obj) -> dict:
    """
    Convert a nested data structure (with explicit or implied key/value pairs) into a tree-like dictionary, applying a given function to terminal values.
            
    Parameters
    ----------
    func : Callable[..., Any]
        _description_
    obj : 
        _description_
    
    Returns
    -------
    dict: 
        _description_
        
    Examples
    --------
    Define the data
    >>> nested_data =  {'type': 'album', 'url': 'link.com', 'audio_features': [
    ...     {'loudness': -11.4, 'duration_ms': 251},
    ...     {'loudness': -15.5, 'duration_ms': 284}]}
    >>> print(nested_data)
    {'type': 'album', 'url': 'link.com', 'audio_features': [{'loudness': -11.4, 'duration_ms': 251}, {'loudness': -15.5, 'duration_ms': 284}]}
    
    Convert to json-friendly representation
    >>> serialized = apply_recursive(str, nested_data)
    >>> print(serialized)
    {'type': 'album', 'url': 'link.com', 'audio_features': {1: {'loudness': '-11.4', 'duration_ms': '251'}, 2: {'loudness': '-15.5', 'duration_ms': '284'}}}
    
    Convert to field/type pairs
    >>> schema = apply_recursive(lambda x: type(x).__name__, nested_data)
    >>> print(schema)
    {'type': 'str', 'url': 'str', 'audio_features': {1: {'loudness': 'float', 'duration_ms': 'int'}, 2: {'loudness': 'float', 'duration_ms': 'int'}}}
    """
    # Handle dictionary-like objects
    if hasattr(obj, 'items'):
        return {key: apply_recursive(func, value) 
                for key, value in obj.items()}
                
    # Handle list-like objects
    elif isinstance(obj, (list, tuple, set)):
        return {key: apply_recursive(func, value) 
                for key, value in list_to_dict(obj, max_items=5).items()}
                
    # Handle base cases
    elif isinstance(obj, str):
        return func(obj)
    else:
        return func(obj)


def schema_jsonify(obj: dict) -> dict:
    r"""
    _summary_

    Parameters
    ----------
    schema : dict
        _description_

    Returns
    -------
    dict : _description_
    
    Examples
    --------
    >>> original_schema = {'name': 'str', 'quantity': 'int', 'features': {1: {'volume': 'str', 'duration': 'float'}, 2: {'volume': 'str', 'duration': 'float'}}, 'creator': {'person': {'name': 'str'}, 'company': {'name': 'str', 'location': 'str'}}}
    >>> schema = schema_jsonify(original_schema)
    >>> schema = {**{"title": "title", "description": "description"}, **schema}
    >>> pprint.pp(schema, compact=True, depth=3)
    {'title': 'title',
     'description': 'description',
     'type': 'object',
     'properties': {'name': {'type': 'string'},
                    'quantity': {'type': 'number'},
                    'features': {'type': 'array',
                                 'minItems': 1,
                                 'maxItems': 2,
                                 'uniqueItems': True,
                                 'items': {...}},
                    'creator': {'type': 'object',
                                'properties': {...},
                                'required': [...]}},
     'required': ['name', 'quantity', 'features', 'creator']}
    """
    schema = {}
    is_dict = isinstance(obj, dict)
    
    # Case 1 (array-like)    
    if obj and is_dict and isinstance(list(obj.keys())[0], int):
        field_len = list(obj.keys())[-1]
        schema = {
            "type": 'array', # coerced to object; includes tuple/list
            "minItems": 1,
            "maxItems": field_len,
            "uniqueItems": True
        }
        # Recurse on first item, assuming homogeneity for simplicity
        schema["items"] = schema_jsonify(obj[1])
        return schema
    
    # Case 2 (dictionary) 
    elif obj and is_dict:
        schema["type"] = "object"
        schema["properties"] = {}
        # Require all by default to easily edit later
        schema["required"] = list(obj.keys())
        
        for key, val in obj.items():
            # Recurse on each value
            schema["properties"][key] = schema_jsonify(val)
        return schema
    
    # Base cases (non-container types)
    # "str" -> "string"
    elif obj == "str": 
        schema["type"] = "string"
        return schema

    # "int"/"float" -> "number"
    elif obj in ("int", "float"): 
        schema["type"] = "number"
        return schema
    
    else:
        schema["type"] = "null"
        return schema


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
    
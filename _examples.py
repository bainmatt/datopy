"""
A home for one-off tests and data-generating routines.
"""

import re
import pprint
import copy
import doctest
import json
import pandas as pd

from typing import List, Literal, Union, Tuple, NamedTuple
from collections import namedtuple
from jsonschema import validate
from dataclasses import dataclass, asdict
from pydantic import BaseModel, ValidationError, PositiveInt

import wptools
import spotipy
import imdb

from spotipy.oauth2 import SpotifyClientCredentials
from imdb import Cinemagoer
from bs4 import BeautifulSoup

import _settings

from nb_utils import doctest_function
from datamodel_utils import (
    iterable_to_schema, 
    _serialize_scraped_data, _list_to_dict, _compare_dict_keys,
    _omit_patterns
)

# Define object types for metadata retrieval
Film = NamedTuple('Film', [('title', str)])
Album = NamedTuple('Album', [('artist', str), ('title', str)])
Book = NamedTuple('Book', [('title', str)])


# ---------------
# --- Helpers ---
# ---------------

def _extract_datadict(
    obj, 
    special_types: Tuple[type] = (dict,), verbose: bool = False) -> tuple:
    """
    Extract data dictionary elements  json-style schema of (key, type)/(key, value) pairs and a df.
    
    Parameters
    ----------
    obj : 
        __description__
    special_types : Tuple[type]
        __description__
    verbose : bool, default=False
    
    Returns
    -------
    schema : 
        __description__
    serialized_dict : 
        __description__    
    schema : 
        __description__    
    """
    schema = iterable_to_schema(obj, special_types)
    serialized_dict = json.dumps(_serialize_scraped_data(obj), indent=4)
    parsed_dict = json.loads(serialized_dict)
    normalized_dict = pd.json_normalize(parsed_dict)
    
    if verbose:
        pprint.pp(schema, depth=5)
        pprint.pp(dict(obj), depth=5)
        pprint.pp(normalized_dict.T[0], compact=True)
    
    return schema, serialized_dict, normalized_dict


def _save_scraped_datadict(
    schema: dict, serialized_dict: dict, normalized_dict: dict,
    source: str, title: str) -> None:
    """
    Save json-style schema of (key, type)/(key, value) pairs and a df.
    """
    title = title.replace(' ', '_')
    
    schema_path = f"output/{source}_{title}_schema.json"
    with open(schema_path, "w") as json_file:
        json.dump(schema, json_file, indent=7)

    obj_path = f"output/{source}_{title}_obj.json"
    with open(obj_path, "w") as json_file:
        json_file.write(serialized_dict)
                    
    df_path = f"output/{source}_{title}_df.csv"
    normalized_dict.to_csv(df_path, index=False, header=True)
                
    return None


# --------------------------------------------
# --- Data dictionary retrieval/extraction ---
# --------------------------------------------
    
def run_scraped_datadict_example(
    source: Literal['imdb', 'spotify', 'wiki'], 
    search_terms: Film | Album | Book,
    special_types: Tuple[type] = (
        dict, imdb.Person.Person, imdb.Movie.Movie, imdb.Company.Company
    ),
    verbose: bool = False,
    do_save: bool = False) -> namedtuple:   
    
    
    
    r"""
    Auto-generate and save an exemplar data dictionary from the metadata of an arbitrary API-extracted data structure.
    
    Parameters
    ----------
    source : Literal['imdb', 'spotify', 'wiki']) 
        The source from which to retrieve data about the requested topic. 
    search_terms : Film | Album | Book
        A namedtuple of required properties (e.g., title) for the topic query.
    special_types : Tuple[type], default=(
        dict, imdb.Person.Person, imdb.Movie.Movie, imdb.Company.Company
        )
        Adds support for datatypes unique to the API of the provided source.
    verbose : bool, default=False
        Option to enable printouts of the retrieved data and schema.
    do_save : bool, default=False
        Option to enable saving of the retrieved data and schema.
 
    Returns
    -------
    obj : 
        __description__
    (__tuple__) : 
        Output of _extract_datadict.
        
    Examples
    --------
    imdb: film
    >>> film = Film("eternal sunshine of the spotless mind")
    >>> outputs = run_scraped_datadict_example(
    ...    source="imdb", search_terms=film, do_save=True)
    >>> dict(outputs.obj)['genres']
    ['Drama', 'Romance', 'Sci-Fi']
    >>> outputs.schema['genres']
    {1: 'str', 2: 'str', 3: 'str'}
    >>> outputs.normalized_dict['composer'][0]
    ['Jon Brion']
    
    spotify: album
    >>> album = Album("radiohead", "kid A")
    >>> outputs = run_scraped_datadict_example(
    ...    source="spotify", search_terms=album, do_save=True)
    >>> outputs.obj['total_tracks']
    11
    >>> outputs.schema['total_tracks']
    'int'
    >>> outputs.normalized_dict['id'][0]
    '6GjwtEZcfenmOf6l18N7T7'
    
    wiki: novel
    >>> book = Book("to kill a mockingbird")
    >>> outputs = run_scraped_datadict_example(
    ...    source="wiki", search_terms=book, do_save=True)
    >>> re.search(r'\[\[(.*?)\]\]', outputs.obj['author']).group(1)
    'Harper Lee'
    >>> outputs.schema['author']
    'str'
    >>> outputs.normalized_dict['pages'][0]
    '281'
    
    wiki: film
    >>> film = Film("eternal sunshine of the spotless mind")
    >>> outputs = run_scraped_datadict_example(
    ...    source="wiki", search_terms=film, do_save=True)
    >>> re.search(r'\[\[(.*?) \]\]', outputs.obj['director']).group(1)
    'Michel Gondry'
    >>> outputs.schema['director']
    'str'
    >>> outputs.normalized_dict['budget'][0]
    '$20 million'
    
    wiki: album
    >>> album = Album("radiohead", "kid A")
    >>> outputs = run_scraped_datadict_example(
    ...    source="wiki", search_terms=album, do_save=True)
    >>> genres_raw = outputs.obj['genre']
    >>> patterns_to_omit = ["[[", "* ", " * ", "\n", "{{nowrap|", "}}"]
    >>> genres_processed = _omit_patterns(genres_raw, patterns_to_omit)
    >>> print(genres_processed.replace("]]", ", ").rstrip(", "))
    Experimental rock, post-rock, art rock, electronica
    >>> outputs.schema['genre']
    'str'
    >>> outputs.normalized_dict['type'][0]
    'studio'
    
    """
    # Check assumptions
    source = str(source).lower()
    message = "Source must be either 'imdb', 'spotify', or 'wiki'."
    assert source in ['imdb', 'spotify', 'wiki'], message
    
    # Normalize query strings
    search_terms = search_terms._replace(
        **{key: str(value).lower() 
           for key, value in search_terms._asdict().items()})
    
    # TODO refactor retrieval using retrieve method of resp Processor subclasses
    # Movie
    if source == 'imdb':
        ia = Cinemagoer()
        movies = ia.search_movie(search_terms.title)
        obj = ia.get_movie(movies[0].movieID)
    
    # Album
    elif source == 'spotify':    
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials()
        )
        results = sp.search(
            q=f'artist:{search_terms.artist} album:{search_terms.title}', type='album'
        )
        album_results = results['albums']['items'][0]
        album_id = album_results['id']
        album_details = sp.album(album_id)
        tracks = sp.album_tracks(album_id)['items']        
        
        # Retrieve additional track details
        track_audio_features = []
        track_streams = []
        for track_num, track_info in enumerate(tracks, start=1):
            track_id = track_info['id']
            # sp.audio_analysis(track_id)
            track_audio_features.append(sp.audio_features(track_id)[0])
            track_streams.append(sp.track(track_id)['popularity'])

        track_audio_features = _list_to_dict(track_audio_features)
        track_streams = _list_to_dict(track_streams)
        
        # Merge album details with additional track details
        obj = copy.deepcopy(album_details)
        obj['track_audio_features'] = track_audio_features
        obj['track_streams'] = track_streams
        
    # Books etc.
    elif source == 'wiki':
        obj = wptools.page(search_terms.title).get_parse().data['infobox']
    
    else: 
        return None
    
    # Extract & save
    schema, serialized_dict, normalized_dict = _extract_datadict(
        obj, special_types, verbose)
    
    if do_save:
        _save_scraped_datadict(schema, serialized_dict, normalized_dict, 
                               source, search_terms.title)
    else:
        pass
    
    Outputs = namedtuple(
        'Outputs', ['obj', 'schema', 'serialized_dict', 'normalized_dict'])
    
    return Outputs(obj, schema, serialized_dict, normalized_dict)


# ---------------------------------------
# --- Data model and validation stuff ---
# ---------------------------------------

# TODO finish example from `datamodel_utils` 'Data validation scheme'

# Movie(**schema)  



if __name__ == "__main__":    
    # Comment out (2) to run all tests in script; (1) to run specific tests
    # doctest.testmod(verbose=True)
    doctest_function(run_scraped_datadict_example, globs=globals())
            
    ## One-off tests
    pass
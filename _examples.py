"""
A home for one-off tests and data-generating routines.

# --- My retrieve/process/load (ETL) & model/validation process for APIs ---
# 1a) Identify your topic, fields of interest, source, and tools
# 1b) Access the relevant API and familiarize
# 2a) Implement a quick-and-dirty Processor subclass for retrieved objects
# 2b) Construct 1-2 representative examples for testing and documentation
# 3a) Implement a Pydantic data model that is robust and reflects your needs
# 3b) Refine your quick-and-dirty Processor and incorporate data validation
# Play around with the data before moving on to more sophisticated analysis
"""

import re
import pprint
import copy
import doctest
import json
import pandas as pd

from typing import List, Literal, Union, Tuple, NamedTuple
from collections import namedtuple
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

import _settings

from nb_utils import doctest_function
from datamodel_utils import (
    apply_recursive, schema_jsonify,
    list_to_dict, omit_string_patterns
)

# Define object types for metadata retrieval
FilmQuery = NamedTuple('FilmQuery', [('title', str)])
AlbumQuery = NamedTuple('Album', [('artist', str), ('title', str)])
BookQuery = NamedTuple('Book', [('title', str)])

DataModel = namedtuple('DataModel', ['obj', 'schema', 'json_schema',
                                     'serialized', 'normalized'])

# TODO add 'see also' sections for required imports from other modules in proj
# TODO rename this to _example_auto_datamodels ?


# ---------------
# --- Helpers ---
# ---------------

# TODO refactor later into SubProcessor

def spotify_album_retrieve(album: AlbumQuery) -> dict:
    """Spotify album metadata retrieval routine."""
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials()
    )
    results = sp.search(
        q=f'artist:{album.artist} album:{album.title}', type='album'
    )    
    if results['albums']['total'] == 0:
        raise LookupError(f"No result found for {album}.")
            
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

    track_audio_features = list_to_dict(track_audio_features)
    track_streams = list_to_dict(track_streams)
            
    # Merge album details with additional track details
    obj = copy.deepcopy(album_details)
    obj['track_audio_features'] = track_audio_features
    obj['track_streams'] = track_streams
    
    return obj


def imdb_film_retrieve(film: FilmQuery) -> dict: 
    """IMDb film metadata retrieval routine."""
    ia = Cinemagoer()
    movies = ia.search_movie(film.title)
    if not movies:
        raise LookupError(f"No result found for {film}.")
    else:
        obj = ia.get_movie(movies[0].movieID)
        
    return obj


def wiki_metadata_retrieve(query: NamedTuple) -> dict:
    try:
        obj = wptools.page(query.title).get_parse().data['infobox']
    except Exception:
        raise LookupError(f"No result found for {query}.") from None
        
    return obj


def extract_datamodel(obj, verbose: bool = False) -> DataModel:
    """
    Extract data dictionary elements  json-style schema of (key, type)/(key, value) pairs and a df.
    
    Parameters
    ----------
    obj : 
        __description__
    verbose : bool, default=False
    
    Returns
    -------
    schema : 
        __description__
    json_schema : 
        __description__
    obj_serialized : 
        __description__    
    obj_normalized : 
        __description__    
    """
    
    schema = apply_recursive(lambda x: type(x).__name__, obj)
    json_schema = schema_jsonify(schema)
    obj_serialized = json.dumps(apply_recursive(str, obj), indent=4)
    obj_parsed = json.loads(obj_serialized)
    obj_normalized = pd.json_normalize(obj_parsed)
    
    if verbose:
        pprint.pp(dict(obj), depth=5)
        pprint.pp(schema, depth=5)
        pprint.pp(obj_normalized.T[0], compact=True)
    
    return DataModel(obj, schema, json_schema, obj_serialized, obj_normalized)


def save_datamodel(
    schema: dict, json_schema: dict, 
    obj_serialized: dict, obj_normalized: dict,
    source: str, search_terms: NamedTuple) -> None:
    """
    Save json-style schema of (key, type)/(key, value) pairs and a df.
    """
    title = str(search_terms.title).lower().replace(' ', '_')
    medium = type(search_terms).__name__.lower().replace(' ', '_')
    
    schema_path = f"output/{source}_{medium}_schema.json"
    with open(schema_path, "w") as json_file:
        json.dump(schema, json_file, indent=4)

    json_schema_path = f"output/{source}_{medium}_json_schema.json"
    with open(json_schema_path, "w") as json_file:
        json.dump(json_schema, json_file, indent=4)

    obj_path = f"output/{source}_{title}_obj.json"
    with open(obj_path, "w") as json_file:
        json_file.write(obj_serialized)
                    
    df_path = f"output/{source}_{title}_df.csv"
    obj_normalized.to_csv(df_path, index=False, header=True)
                
    return None


# --------------------------------------------
# --- Data dictionary retrieval/extraction ---
# --------------------------------------------

def run_auto_datamodel_example(
    source: Literal['imdb', 'spotify', 'wiki'], 
    search_terms: FilmQuery | AlbumQuery | BookQuery,
    verbose: bool = False,
    do_save: bool = False) -> DataModel:   
    
    r"""
    Auto-generate and save an exemplar data dictionary from the metadata of an arbitrary API-extracted data structure.
    
    Parameters
    ----------
    source : Literal['imdb', 'spotify', 'wiki']) 
        The source from which to retrieve data about the requested topic. 
    search_terms : FilmQuery | AlbumQuery | BookQuery
        A namedtuple of required properties (e.g., title) for the topic query.
    verbose : bool, default=False
        Option to enable printouts of the retrieved data and schema.
    do_save : bool, default=False
        Option to enable saving of the retrieved data and schema.
 
    Returns
    -------
    obj : 
        __description__
    (__tuple__) : 
        Output of extract_datamodel.
        
    Examples
    --------
    setup
    >>> do_save=False
    
    # imdb: film
    # >>> film = FilmQuery("eternal sunshine of the spotless mind")
    # >>> datamodel = run_auto_datamodel_example(
    # ...     source="imdb", search_terms=film, verbose=False, do_save=do_save)
    # >>> dict(datamodel.obj)['genres']
    # ['Drama', 'Romance', 'Sci-Fi']
    # >>> datamodel.schema['genres']
    # {1: 'str', 2: 'str', 3: 'str'}
    # >>> datamodel.normalized['original air date'][0]
    # '19 Mar 2004 (USA)'
    
    spotify: album
    >>> album = AlbumQuery("radiohead", "kid A") 
    >>> datamodel = run_auto_datamodel_example(
    ...     source="spotify", search_terms=album, do_save=do_save)
    >>> datamodel.obj['total_tracks']
    11
    >>> datamodel.schema['total_tracks']
    'int'
    >>> datamodel.normalized['id'][0]
    '6GjwtEZcfenmOf6l18N7T7'
    
    # wiki: novel
    # >>> book = BookQuery("to kill a mockingbird")
    # >>> outputs = run_auto_datamodel_example(
    # ...    source="wiki", search_terms=book, do_save=do_save)
    # >>> re.search(r'\[\[(.*?)\]\]', outputs.obj['author']).group(1)
    # 'Harper Lee'
    # >>> outputs.schema['author']
    # 'str'
    # >>> outputs.normalized['pages'][0]
    # '281'
    
    # wiki: film
    # >>> film = FilmQuery("eternal sunshine of the spotless mind")
    # >>> outputs = run_auto_datamodel_example(
    # ...    source="wiki", search_terms=film, do_save=do_save)
    # >>> re.search(r'\[\[(.*?) \]\]', outputs.obj['director']).group(1)
    # 'Michel Gondry'
    # >>> outputs.schema['director']
    # 'str'
    # >>> outputs.normalized['budget'][0]
    # '$20 million'
    
    # wiki: album
    # >>> album = AlbumQuery("radiohead", "kid A")
    # >>> outputs = run_auto_datamodel_example(
    # ...    source="wiki", search_terms=album, do_save=do_save)
    # >>> genres_raw = outputs.obj['genre']
    # >>> patterns_to_omit = ["[[", "* ", " * ", "\n", "{{nowrap|", "}}"]
    # >>> genres_processed = omit_string_patterns(genres_raw, patterns_to_omit)
    # >>> print(genres_processed.replace("]]", ", ").rstrip(", "))
    # Experimental rock, post-rock, art rock, electronica
    # >>> outputs.schema['genre']
    # 'str'
    # >>> outputs.normalized['type'][0]
    # 'studio'

    """    
    # Check assumptions
    source = str(source).lower()
    message = "Source must be either 'imdb', 'spotify', or 'wiki'."
    assert source in ['imdb', 'spotify', 'wiki'], message
    
    # TODO refactor retrieval using retrieve method of resp Processor subclasses
    # Movie
    if source == 'imdb':
        ia = Cinemagoer()
        movies = ia.search_movie(search_terms.title)
        if not movies:
            raise LookupError(f"No result found for {search_terms}.")
        else:
            obj = ia.get_movie(movies[0].movieID)
    
    # Album
    elif source == 'spotify':    
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials()
        )
        results = sp.search(
            q=f'artist:{search_terms.artist} album:{search_terms.title}', type='album'
        )    
        if results['albums']['total'] == 0:
            raise LookupError(f"No result found for {search_terms}.")
        
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

        track_audio_features = list_to_dict(track_audio_features)
        track_streams = list_to_dict(track_streams)
        
        # Merge album details with additional track details
        obj = copy.deepcopy(album_details)
        obj['track_audio_features'] = track_audio_features
        obj['track_streams'] = track_streams
        
    # Books etc.
    elif source == 'wiki':
        try:
            obj = wptools.page(search_terms.title).get_parse().data['infobox']
        except Exception:
            raise LookupError(f"No result found for {search_terms}.") from None
    
    else: 
        return None
    
    # Extract & save
    datamodel = extract_datamodel(obj, verbose)
    
    if do_save:
        save_datamodel(datamodel.schema, datamodel.json_schema,
                       datamodel.serialized, datamodel.normalized,
                       source, search_terms)
    else:
        pass
    
    return datamodel


# ---------------------------------------
# --- Pitfalls of raw data validation ---
# ---------------------------------------

# --- Data model considerations ---
# - Fields: descriptions, required entries
# - Type-specific: num (range), str (regex), cat (options)
# - List-like container types: uniformity of elements, length, options, order

# Generally opt for manually defined schemas for retrieved data. Data
# is messy and unpredictable and every automated attempt will either screw up 
# edge cases or overlook nuances/quirks (Ex: an integer dressed up as a string,
# masquerading as an iterable).
# 
# Most importantly, do NOT try to validate all the data coming in! Just build a
# robust retrieval system and validate everything before loading into your DBS.
# As cool as it would be to seamlessly validate incoming data against 
# auto-generated schemas, this is (1) really messy and (2) highly unnecessary.
# 
# Instead, use these tools to quickly grasp the structure of retrieved data and 
# build comprehensive Pydantic models that perfectly suit your downstream needs!


# An example of messy, highly unnecessary testing of retrieved data
obj = spotify_album_retrieve(AlbumQuery("radiohead", "kid a"))
with open('output/spotify_album_json_schema.json') as file:
    album_schema = json.load(file)
# This line raises an error
# validate(instance=obj, schema=album_schema)

# An idealized example to demonstrate json validation in theory
with open('models/imdb_model.json') as file:
    movie_schema = json.load(file)

valid_raw_movie = {
    "title": "green eggs and ham", "year": 1904, "kind": "movie", 
    "director": {"1": {"name": "Jill Smith"}}
}

# The second line raises an error
invalid_raw_movie = {"name": 1, "price": 34.99}
validate(instance=valid_raw_movie, schema=movie_schema)
# validate(instance=invalid_raw_movie, schema=movie_schema)


# ---------------------------------
# --- Processed data validation ---
# ---------------------------------


# TODO consider adding later: IUCNSpecies metadata, WBankNation metadata
# TODO place media/animals/nations processors in {media/eco/global}_pulse.py


# TODO implement pydantic data models for processed objects
# TODO 1 valid/invalid validation demo for each (5*2) using pydantic

# Reference: 
class IMDbFilm(BaseModel):
    """
    Data model for processed imdb metadata. 
    Raw data schema reference: 'output/imdb_film_schema.json'
    """
    # fields of interest: 
    
    title: str
    
    
class SpotifyAlbum(BaseModel):
    """
    Data model for processed Spotify metadata. 
    Raw data schema reference: 'output/spotify_album_schema.json'
    """
    # fields of interest: 
    
    title: str
    album_type: str
    

class WikiBook(BaseModel):
    """
    Data model for processed Wikipedia novel metadata. 
    Raw data schema reference: 'output/wiki_book_schema.json'
    """
    # fields of interest: 
        
    title: str


class WikiFilm(BaseModel):
    """
    Data model for processed Wikipedia film metadata. 
    Raw data schema reference: 'output/wiki_film_schema.json'
    """
    # fields of interest: 
            
    title: str


class WikiAlbum(BaseModel):
    """
    Data model for processed Wikipedia album metadata. 
    Raw data schema reference: 'output/wiki_album_schema.json'
    """
    # fields of interest: 
                
    title: str







# XXX rough pydantic validation tests
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



if __name__ == "__main__":    
    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod(verbose=False)
    # doctest_function(run_auto_datamodel_example, globs=globals(), verbose=False)
            
    ## One-off tests
    pass
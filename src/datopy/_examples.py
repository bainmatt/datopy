"""
A home for one-off tests and data-generating routines.
"""

# --- My retrieve/process/load (ETL) & model/validation process for APIs ---
# 1a) Identify your topic, fields of interest, source, and tools
# 1b) Access the relevant API and familiarize
# 2a) Implement a quick-and-dirty Processor subclass for retrieved objects
# 2b) Construct 1-2 representative examples for testing and documentation
# 3a) Implement a Pydantic data model that is robust and reflects your needs
# 3b) Refine your quick-and-dirty Processor and incorporate data validation
# Play around with the data before moving on to more sophisticated analysis

# --- Data model considerations ---
# - Fields: descriptions, required entries
# - Type-specific: num (range), str (regex), cat (options)
# - List-like container types: uniformity of elements, length, options, order


import os
import re
import copy
import json
import pprint
import doctest
import pathlib
import pandas as pd
from jsonschema import validate
from collections import namedtuple
from typing import Literal, NamedTuple

import imdb
import spotipy
import wptools
from imdb import Cinemagoer
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials

# import datopy._settings
from datopy.models.media import Film, Album, Book
from datopy.etl import omit_string_patterns
from datopy.workflow import doctest_function
from datopy.modeling import (
    apply_recursive, list_to_dict, schema_jsonify
)

# Define custom types
DataModel = namedtuple('DataModel', ['obj', 'schema', 'json_schema',
                                     'serialized', 'normalized'])

# Define paths
try:
    # The __file__ variable is only accessible at runtime
    file_dir = pathlib.Path(__file__).parent.resolve()
except NameError:
    # If __file__ is not defined, use a fallback directory
    # cwd = pathlib.Path().resolve()
    file_dir = 'src/datopy/'


# TODO add 'see also' sections for required imports from other modules in proj
# TODO rename this to _example_auto_datamodels ?


# ---------------
# --- Helpers ---
# ---------------

# TODO refactor later into SubProcessor

def spotify_album_retrieve(album: Album) -> dict:
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
    track_audio_features_tmp = []
    track_streams_tmp = []
    for track_num, track_info in enumerate(tracks, start=1):
        track_id = track_info['id']
        # sp.audio_analysis(track_id)
        track_audio_features_tmp.append(sp.audio_features(track_id)[0])
        track_streams_tmp.append(sp.track(track_id)['popularity'])

    track_audio_features = list_to_dict(track_audio_features_tmp)
    track_streams = list_to_dict(track_streams_tmp)

    # Merge album details with additional track details
    obj = copy.deepcopy(album_details)
    obj['track_audio_features'] = track_audio_features
    obj['track_streams'] = track_streams

    return obj


def imdb_film_retrieve(film: Film) -> dict:
    """IMDb film metadata retrieval routine."""
    ia = Cinemagoer()
    movies = ia.search_movie(film.title)
    if not movies:
        raise LookupError(f"No result found for {film}.")
    else:
        obj = ia.get_movie(movies[0].movieID)

    return obj


def wiki_metadata_retrieve(query: Film | Album | Book) -> dict:
    try:
        obj = wptools.page(query.title).get_parse().data['infobox']
    except Exception:
        raise LookupError(f"No result found for {query}.") from None

    return obj


def extract_datamodel(obj, verbose: bool = False) -> DataModel:
    """
    Extract data dictionary elements, a json-style schema of
    (key, type)/(key, value) pairs, and a dataframe entry.

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
    obj_serialized: dict, obj_normalized: pd.DataFrame,
    source: str, search_terms: Film | Album | Book
) -> None:
    """
    Save json-style schema of (key, type)/(key, value) pairs and a df.
    """
    title = str(search_terms.title).lower().replace(' ', '_')
    medium = type(search_terms).__name__.lower().replace(' ', '_')

    schema_path = f"{file_dir}/output/{source}_{medium}_schema.json"
    with open(schema_path, "w") as json_file:
        json.dump(schema, json_file, indent=4)

    json_schema_path = f"output/{source}_{medium}_json_schema.json"
    with open(json_schema_path, "w") as json_file:
        json.dump(json_schema, json_file, indent=4)

    obj_path = f"output/{source}_{title}_obj.json"
    with open(obj_path, "w") as json_file:
        json_file.write(str(obj_serialized))

    df_path = f"output/{source}_{title}_df.csv"
    obj_normalized.to_csv(df_path, index=False, header=True)

    return None


# --------------------------------------------
# --- Data dictionary retrieval/extraction ---
# --------------------------------------------

def run_auto_datamodel_example(
    source: Literal['imdb', 'spotify', 'wiki'],
    search_terms: Film | Album | Book,
    verbose: bool = False,
    do_save: bool = False
) -> DataModel:

    r"""
    Auto-generate and save an exemplar data dictionary from the metadata of
    an arbitrary API-extracted data structure.

    Parameters
    ----------
    source : Literal['imdb', 'spotify', 'wiki'])
        The source from which to retrieve data about the requested topic.
    search_terms : Film | Album | Book
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
    .. doctest::
        :skipif: skip_slow

        Setup

        >>> import re
        >>> from datopy._examples import run_auto_datamodel_example
        >>> from datopy.etl import omit_string_patterns
        >>> from datopy.models.media import Album, Book, Film

        >>> do_save=False

        imdb: film

        >>> film = Film("eternal sunshine of the spotless mind")
        >>> datamodel = run_auto_datamodel_example(
        ...     source="imdb", search_terms=film,
        ...     verbose=False, do_save=do_save)
        >>> dict(datamodel.obj)['genres']
        ['Drama', 'Romance', 'Sci-Fi']
        >>> datamodel.schema['genres']
        {1: 'str', 2: 'str', 3: 'str'}
        >>> datamodel.normalized['original air date'][0]
        '19 Mar 2004 (USA)'

        spotify: album

        ..
            # >>> album = Album("kid A", "radiohead")
            # >>> datamodel = run_auto_datamodel_example(
            # ...     source="spotify", search_terms=album, do_save=do_save)
            # >>> datamodel.obj['total_tracks']
            # 11
            # >>> datamodel.schema['total_tracks']
            # 'int'
            # >>> datamodel.normalized['id'][0]
            # '6GjwtEZcfenmOf6l18N7T7'

        wiki: novel

        >>> book = Book("to kill a mockingbird")
        >>> outputs = run_auto_datamodel_example(
        ...    source="wiki", search_terms=book, do_save=do_save)
        >>> re.search(r'\[\[(.*?)\]\]', outputs.obj['author']).group(1)
        'Harper Lee'
        >>> outputs.schema['author']
        'str'
        >>> outputs.normalized['pages'][0]
        '281'

        wiki: film

        >>> film = Film("eternal sunshine of the spotless mind")
        >>> outputs = run_auto_datamodel_example(
        ...    source="wiki", search_terms=film, do_save=do_save)
        >>> re.search(r'\[\[(.*?) \]\]', outputs.obj['director']).group(1)
        'Michel Gondry'
        >>> outputs.schema['director']
        'str'
        >>> outputs.normalized['budget'][0]
        '$20 million'

        wiki: album

        >>> album = Album("kid A", "radiohead")
        >>> outputs = run_auto_datamodel_example(
        ...    source="wiki", search_terms=album, do_save=do_save)
        >>> genres_raw = outputs.obj['genre']
        >>> patterns_to_omit = ["[[", "* ", " * ", "\n", "{{nowrap|", "}}"]
        >>> genres_processed = omit_string_patterns(
        ...     genres_raw, patterns_to_omit)
        >>> print(genres_processed.replace("]]", ", ").rstrip(", "))
        Experimental rock, post-rock, art rock, electronica, alternative rock
        >>> outputs.schema['genre']
        'str'
        >>> outputs.normalized['type'][0]
        'studio'

    """
    # Check assumptions
    # TODO remove line below (redundant)
    # source = str(source).lower()
    message = "Source must be either 'imdb', 'spotify', or 'wiki'."
    assert source in ['imdb', 'spotify', 'wiki'], message

    # TODO refactor retrieval w/ retrieve method of resp Processor subclasses
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
            q=f'artist:{search_terms.artist} album:{search_terms.title}',
            type='album'
        )
        if results['albums']['total'] == 0:
            raise LookupError(f"No result found for {search_terms}.")

        album_results = results['albums']['items'][0]
        album_id = album_results['id']
        album_details = sp.album(album_id)
        tracks = sp.album_tracks(album_id)['items']

        # Retrieve additional track details
        track_audio_features_tmp = []
        track_streams_tmp = []
        for track_num, track_info in enumerate(tracks, start=1):
            track_id = track_info['id']
            # sp.audio_analysis(track_id)
            track_audio_features_tmp.append(sp.audio_features(track_id)[0])
        track_streams_tmp.append(sp.track(track_id)['popularity'])

        track_audio_features = list_to_dict(track_audio_features_tmp)
        track_streams = list_to_dict(track_streams_tmp)

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
# Instead use these tools to quickly grasp the structure of retrieved data and
# build comprehensive Pydantic models that fully suit your downstream needs!

# An example of messy, highly unnecessary testing of retrieved data
def _run_messy_example():
    # obj = spotify_album_retrieve(Album("kid a", "radiohead"))
    fname = 'output/spotify_album_json_schema.json'
    with open(os.path.join(file_dir, fname)) as file:
        album_schema = json.load(file)
    return album_schema
    # This line raises an error
    # validate(instance=obj, schema=album_schema)


def _run_idealized_example():
    # An idealized example to demonstrate json validation in theory
    fname = 'models/output/imdb_model.json'
    with open(os.path.join(file_dir, fname)) as file:
        movie_schema = json.load(file)

    valid_raw_movie = {
        "title": "green eggs and ham", "year": 1904, "kind": "movie",
        "director": {"1": {"name": "Jill Smith"}}
    }

    # The second line raises an error
    # invalid_raw_movie = {"name": 1, "price": 34.99}
    validate(instance=valid_raw_movie, schema=movie_schema)
    # validate(instance=invalid_raw_movie, schema=movie_schema)

    return movie_schema, valid_raw_movie

# ---------------------------------
# --- Processed data validation ---
# ---------------------------------

# TODO consider adding later: IUCNSpecies metadata, WBankNation metadata
# IUCN: https://pypi.org/project/IUCN-API/
# Consult: https://www.kaggle.com/code/saiulluri/creating-a-wildlife-database
# WBank: https://pypi.org/project/wbgapi/#description


if __name__ == "__main__":
    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod(verbose=True)
    # doctest_function(run_auto_datamodel_example, globs=globals(),verbose=False)

    # One-off tests
    pass

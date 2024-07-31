"""
A home for one-off tests and data-generating routines.

.. warning:: The contents of this module will be moved in a future release.
"""

# -- My retrieve/process/load (ETL) & model/validation process for APIs ------
#
#   1a) Identify your topic, fields of interest, source, and tools
#   1b) Access the relevant API and familiarize
#   2a) Implement a quick-and-dirty Processor subclass for retrieved objects
#   2b) Construct 1-2 representative examples for testing and documentation
#   3a) Implement a Pydantic data model that is robust and reflects your needs
#   3b) Refine your quick-and-dirty Processor and incorporate data validation
#   Play around with the data before moving on to more sophisticated analysis.
#
# -- Data model considerations -----------------------------------------------
#
#   * Fields: descriptions, required entries
#   * Type-specific: num (range), str (regex), cat (options)
#   * List-like container types: uniformity of elements, length, options, order


# -- Custom types ------------------------------------------------------------

import os
import re
import sys
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
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# import datopy._settings
from datopy.etl import omit_string_patterns
from datopy.workflow import doctest_function
from datopy.modeling import (
    apply_recursive, list_to_dict, schema_jsonify
)
from datopy.util._decorators import add_wip, doc
from datopy.util._numpydoc_validate import numpydoc_validate_module


# TODO: rename this to _example_auto_datamodels ?


# -- Custom types ------------------------------------------------------------


class MediaQuery(NamedTuple):
    """
    Query object types for media metadata retrieval.
    """
    title: str
    artist: str | None = None


DataModel = namedtuple(
    'DataModel', ['obj', 'schema', 'json_schema', 'serialized', 'normalized']
)
"""
Custom data model return type.
"""


Film = type('Film', (MediaQuery,), {})
Album = type('Album', (MediaQuery,), {})
Book = type('Book', (MediaQuery,), {})


# ----------------------------------------------------------------------------


# TODO: put these into paths.py and adjust according to notes


def find_project_root():
    """
    Obtain an absolute path to the project root for saving and loading.

    Notes
    -----
    To set your project root explicitly as an environment variable, run::

        os.environ["PROJECT_ROOT"] = "/path/to/src/pkg"

    Examples
    --------
    >>> from datopy._examples import find_project_root
    >>> import pathlib

    >>> project_root = find_project_root()
    >>> input_dir = pathlib.Path(project_root, "input")
    >>> output_dir = pathlib.Path(project_root, "output")
    >>> pathlib.Path(*input_dir.parts[-3:])
    PosixPath('src/datopy/input')
    >>> pathlib.Path(*output_dir.parts[-3:])
    PosixPath('src/datopy/output')
    """
    load_dotenv()

    # Obtain an absolute path to the project root (typically src/<pkgname>)
    try:
        # The __file__ variable is only accessible at runtime
        project_root = pathlib.Path(__file__).parent.resolve()
    except NameError:
        # If __file__ is not defined (running in console), use a fallback
        print("Using fallback project directory\n")
        project_root = pathlib.Path('datopy').resolve()

    # Override with an environment variable if defined
    project_root = os.getenv("PROJECT_ROOT", default=project_root)
    return pathlib.Path(project_root).resolve()


# ----------------------------------------------------------------------------


# TODO: place these demos in a new module to illustrate docstring decorators


# @add_wip
@doc(kw1="root")
def _root_function(x: int, y: int):
    """
    Apply my function to {kw1}.

    .. note:: WIP.

    Parameters
    ----------
    x : int
        Argument x of {kw1}.
    y : int
        Argument y of {kw1}.
    """
    pass


@doc(_root_function, kw1="leaf 1")
def _leaf_1(x: int, y: int, z: int):
    """
    z : int
        Argument z of {kw1}.

    Notes
    -----
    This is an extension of :func:`root_function`'s documentation.
    """
    pass


@doc(_root_function, kw1="leaf 2")
def _leaf_2(x: int, y: int):
    """
    Examples
    --------
    >>> x = 4
    >>> y = 5
    >>> x + y
    9
    """
    pass


# -- Helpers -----------------------------------------------------------------


# TODO: refactor later into SubProcessor


def spotify_album_retrieve(album: Album) -> dict:
    """
    Retrieve metadata for a given musical album via Spotify.
    """
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
    """
    IMDb film metadata retrieval routine.
    """
    ia = Cinemagoer()
    movies = ia.search_movie(film.title)
    if not movies:
        raise LookupError(f"No result found for {film}.")
    else:
        obj = ia.get_movie(movies[0].movieID)

    return obj


def wiki_metadata_retrieve(query: Film | Album | Book) -> dict:
    """
    Extract metadata for the supplied work.

    Parameters
    ----------
    query : Film | Album | Book
        The work to be inexed.

    Returns
    -------
    dict
        A dictionary containing metadata retrieved from the Wikipedia infobox.
    """
    try:
        obj = wptools.page(query.title).get_parse().data['infobox']
    except Exception:
        raise LookupError(f"No result found for {query}.") from None

    return obj


def extract_datamodel(obj, verbose: bool = False) -> DataModel:
    """
    Construct a data model from a scraped data structure.

    The constructed objects include dictionary elements,
    a json-style schema of (key, type)/(key, value) pairs,
    and a dataframe entry.

    Parameters
    ----------
    obj : __type__
        __description__.

    verbose : bool, default=False
        An option to enable/disable printing of outputs.

    Returns
    -------
    DataModel
        A dictionary containing the fields: ``schema``, ``json_schema``, ``obj_serialized``, and ``obj_normalized``.
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

    schema_path = f"{find_project_root()}/output/{source}_{medium}_schema.json"
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


# -- Data dictionary retrieval/extraction ------------------------------------


def run_auto_datamodel_example(
    source: Literal['imdb', 'spotify', 'wiki'],
    search_terms: Film | Album | Book,
    verbose: bool = False,
    do_save: bool = False
) -> DataModel:
    r"""
    Generate an exemplar data model from an API-extracted data structure.

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
    DataModel
        The output of ``extract_datamodel``.

    Examples
    --------
    .. code-block:: python doctest

    Setup

    >>> import re
    >>> from datopy._examples import run_auto_datamodel_example
    >>> from datopy.etl import omit_string_patterns
    >>> from datopy._examples import Album, Book, Film

    >>> do_save=False

    IMDb film

    .. doctest::
        :skipif: skip_slow

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

    Spotify album

    .. doctest::
        :skipif: skip_slow

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

    Wikipedia novel

    .. doctest::
        :skipif: skip_slow

        >>> book = Book("to kill a mockingbird")
        >>> outputs = run_auto_datamodel_example(
        ...    source="wiki", search_terms=book, do_save=do_save)
        >>> re.search(r'\[\[(.*?)\]\]', outputs.obj['author']).group(1)
        'Harper Lee'
        >>> outputs.schema['author']
        'str'
        >>> outputs.normalized['pages'][0]
        '281'

    Wikipedia film

    .. doctest::
        :skipif: skip_slow

        >>> film = Film("eternal sunshine of the spotless mind")
        >>> outputs = run_auto_datamodel_example(
        ...    source="wiki", search_terms=film, do_save=do_save)
        >>> re.search(r'\[\[(.*?) \]\]', outputs.obj['director']).group(1)
        'Michel Gondry'
        >>> outputs.schema['director']
        'str'
        >>> outputs.normalized['budget'][0]
        '$20 million'

    Wikipedia album

    .. doctest::
        :skipif: skip_slow

        >>> album = Album("kid A", "radiohead")
        >>> outputs = run_auto_datamodel_example(
        ...    source="wiki", search_terms=album, do_save=do_save)
        >>> genres_raw = outputs.obj['genre']
        >>> patterns_to_omit = ["[[", "* ", " * ", "\n", "{{nowrap|", "}}"]
        >>> genres_processed = omit_string_patterns(
        ...     genres_raw, patterns_to_omit)
        >>> print(genres_processed.replace("]]", ", ").rstrip(", "))
        Experimental rock, post-rock, art rock, electronica
        >>> outputs.schema['genre']
        'str'
        >>> outputs.normalized['type'][0]
        'studio'
    """
    # Check assumptions
    # TODO: remove line below (redundant)
    # source = str(source).lower()
    message = "Source must be either 'imdb', 'spotify', or 'wiki'."
    assert source in ['imdb', 'spotify', 'wiki'], message

    # TODO: refactor retrieval w/ retrieve method of resp Processor subclasses
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


# -- Pitfalls of raw data validation -----------------------------------------
#
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
#
# ----------------------------------------------------------------------------


def _run_messy_example():
    """
    An example of messy, highly unnecessary testing of retrieved data.
    """
    # obj = spotify_album_retrieve(Album("kid a", "radiohead"))
    fname = 'output/spotify_album_json_schema.json'
    with open(os.path.join(find_project_root(), fname)) as file:
        album_schema = json.load(file)
    return album_schema
    # This line raises an error
    # validate(instance=obj, schema=album_schema)


def _run_idealized_example():
    """
    An idealized example to demonstrate json validation in theory.
    """
    fname = 'models/output/imdb_model.json'
    with open(os.path.join(find_project_root(), fname)) as file:
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


# -- Processed data validation -----------------------------------------------


# TODO: consider adding later: IUCNSpecies metadata, WBankNation metadata
# IUCN: https://pypi.org/project/IUCN-API/
# Consult: https://www.kaggle.com/code/saiulluri/creating-a-wildlife-database
# WBank: https://pypi.org/project/wbgapi/#description


if __name__ == "__main__":
    # Comment out (2) to run all tests in script; (1) to run specific tests
    # doctest.testmod(verbose=True)
    # doctest_function(find_project_root, globs=globals(),verbose=False)

    skip = ["Album", "Book", "Film", "DataModel", "MediaQuery"]
    numpydoc_validate_module(sys.modules['__main__'], excluded_objects=skip)

    pass

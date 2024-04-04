"""
A home for one-off tests and data-generating routines.
"""

import re
import pprint
import copy
import json
import pandas as pd

from typing import Literal, Union
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
from datamodel_utils import iterable_to_schema, _serialize_scraped_data


# ---------------
# --- Helpers ---
# ---------------

def _save_scraped_data(
    schema: dict, serialized_dict: dict, 
    normalized_dict: dict,
    source: Literal['imdb', 'spotify', 'wiki']) -> None:
    """Save json-style schema of (key, type)/(key, value) pairs and a df.
    """
    schema_path = f"output/{source}_schema.json"
    with open(schema_path, "w") as json_file:
        json.dump(schema, json_file, indent=7)

    obj_path = f"output/{source}_obj.json"
    with open(obj_path, "w") as json_file:
        json_file.write(serialized_dict)
                
    df_path = f"output/{source}_df.csv"
    normalized_dict.to_csv(df_path, index=False, header=True)
            
    return None

# ------------------------
# --- Data model files ---
# ------------------------
    
## Movie
def imdb_datadict_example(verbose: bool = False) -> tuple:
    """Auto-generate exemplar data dictionary for an arbitrary imdb object.
    """
    special_types = (
        dict, imdb.Person.Person, imdb.Movie.Movie, imdb.Company.Company
    )
    
    ia = Cinemagoer()
    movies = ia.search_movie('castlevania')
    imdb_obj = ia.get_movie(movies[0].movieID)

    schema = iterable_to_schema(imdb_obj, special_types)
    serialized_dict = json.dumps(_serialize_scraped_data(imdb_obj), indent=4)
    parsed_dict = json.loads(serialized_dict)
    normalized_dict = pd.json_normalize(parsed_dict)
    
    if verbose:
        pprint.pp(schema, depth=3)
        pprint.pp(dict(imdb_obj), depth=3)
        pprint.pp(pd.json_normalize(schema).T[0], compact=True)
    
    return schema, serialized_dict, normalized_dict


# TODO finish this
## Album
def spotify_datadict_example(verbose: bool = False) -> tuple:   
    """Auto-generate exemplar data dictionary for an arbitrary Spotify object.
    """ 
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = sp.search(q=f'artist:{"radiohead"} album:{"kid A"}', type='album')
    spotify_obj = results['albums']['items'][0]
    # Contains additional info absent from `spotify_obj`
    album_details = sp.album(spotify_obj['id'])

    ...


# TODO finish this    
## Wikipedia
# my_wiki_obj = wptools.page("Canada").get_parse().data['infobox']
# schema = iterable_to_schema(my_wiki_obj, special_types)
    

# ---------------------------------------
# --- Data model and validation stuff ---
# ---------------------------------------

# TODO finish example from `datamodel_utils` 'Data validation scheme'

# Movie(**schema)  


if __name__ == "__main__":    
    # schema, serialized_dict, norm_dict = imdb_datadict_example(verbose=True)
    # _save_scraped_data(schema, serialized_dict, norm_dict, 'imdb')
    pass
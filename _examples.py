"""
A home for one-off tests and data-generating routines.
"""

import re
import pprint
import json
import pandas as pd

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


# ------------------------
# --- Data model files ---
# ------------------------
special_types = (
    dict, imdb.Person.Person, imdb.Movie.Movie, imdb.Company.Company
)
    
# Movie
def imdb_datadict_example(verbose: bool = False) -> tuple:
    ia = Cinemagoer()
    movies = ia.search_movie('castlevania')
    my_imdb_obj = ia.get_movie(movies[0].movieID)

    schema = iterable_to_schema(my_imdb_obj, special_types)
    serialized_dict = json.dumps(_serialize_scraped_data(my_imdb_obj), indent=4)
    parsed_dict = json.loads(serialized_dict)
    normalized_dict = pd.json_normalize(parsed_dict)
    
    if verbose:
        pprint.pp(dict(my_imdb_obj), depth=3)
        pprint.pp(schema, depth=3)
        pprint.pp(pd.json_normalize(schema).T[0], compact=True)
    
    return schema, serialized_dict, normalized_dict
    
    
def save_scraped_data(schema, serialized_dict, normalized_dict):
    schema_path = "output/imdb_schema.json"
    with open(schema_path, "w") as json_file:
        json.dump(schema, json_file, indent=7)

    obj_path = "output/imdb_obj.json"
    with open(obj_path, "w") as json_file:
        json_file.write(serialized_dict)
        
    df_path = "output/imdb_df.csv"
    normalized_dict.to_csv(df_path, index=False, header=True)
    
    return None
    
# schema, serialized_dict, normalized_dict = imdb_datadict_example(verbose=True)
# save_scraped_data(schema, serialized_dict, normalized_dict)


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
    

# ---------------------------------------
# --- Data model and validation stuff ---
# ---------------------------------------

# XXX 

# Movie(**schema)  
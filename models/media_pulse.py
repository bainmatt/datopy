"""
__summary__

--- Execution guidelines ---
To run a module within a subfolder that relies on modules in a parent folder:
- Ensure your working directory is set to your project parent directory.
- Always use absolute imports. The debugger will execute from the parent.
- Do not rely on the 'Run Python File in Dedicated Terminal' procedure. Instead:
- Set up a project_dir/.vscode/launch.json file containing the configuration:
{
    "name": "Python: Current File (Integrated Terminal)",
    "type": "debugpy",
    "request": "launch",
    "program": "${file}",
    "cwd": "${workspaceFolder}",
    "env": {
        "PYTHONPATH": "${workspaceFolder}"
    },
    "console": "integratedTerminal"
}
- Use this configuration to execute and debug files in context.
- To execute modules directly from the Debug Console or Integrated Terminal:
>> python -m {directory}.{module}
"""

import re
import pprint
import copy
import doctest
import json
import pandas as pd

from typing import List, Literal, Union, Tuple, NamedTuple, Optional, Annotated
from collections import namedtuple
from datetime import datetime
from jsonschema import validate
from dataclasses import dataclass, asdict
from pydantic import BaseModel, ValidationError, PositiveInt, Field, constr

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
    list_to_dict, omit_string_patterns,
    CustomTypes, BaseProcessor
)


# --------------------------
# --- Metadata retrieval ---
# --------------------------

class MediaQuery:
    """
    Query object types for media metadata retrieval.
    """
    Film = NamedTuple('Film', [('title', str)])
    Album = NamedTuple('Album', [('artist', str), ('title', str)])
    Book = NamedTuple('Book', [('title', str)])


class IMDbFilm(BaseModel):
    """
    Data model for processed imdb metadata. 
    
    Example
    -------
    >>> valid_film = IMDbFilm(
    ...     title='name 10!', imdb_id='tt1234567', kind='movie',
    ...     year=1990, rating=7.2, votes=122,
    ...     genres='romantic comedy, thriller', cast='mrs smith,mr smith',
    ...     plot='alas! once upon a time, ...',
    ...     budget_mil=1123929)
    
    >>> invalid_film = dict(
    ...     title='name', imdb_id='tt12', year=1975, votes=-2, rating=5.0)
    >>> try: 
    ...     IMDbFilm(**invalid_film)
    ... except ValidationError as e: 
    ...     print(e)          # use pprint.pp(e.errors()) for easy-to-read list
    3 validation errors for IMDbFilm
    imdb_id
      String should match pattern '^tt.*\d{7}$' [type=string_pattern_mismatch, input_value='tt12', input_type=str]
        For further information visit https://errors.pydantic.dev/2.6/v/string_pattern_mismatch
    kind
      Field required [type=missing, input_value={'title': 'name', 'imdb_i...tes': -2, 'rating': 5.0}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.6/v/missing
    votes
      Input should be greater than or equal to 0 [type=greater_than_equal, input_value=-2, input_type=int]
        For further information visit https://errors.pydantic.dev/2.6/v/greater_than_equal
    
    Survey available fields and types
    # >>> film = imdb_film_retrieve(Film('spirited away'))
    # >>> film.keys()
    # >>> pprint.pp(apply_recursive(lambda x: type(x).__name__, film), depth=3)
    """
    # Identifiers
    title: CustomTypes.CSVnumstr
    imdb_id: str = Field(pattern=r'^tt.*\d{7}$',
                         description="Unique 7-digit IMDb tt identifier")
    kind: CustomTypes.CSVstr = Field(examples=['movie', 'tv series'],
                                     description="Retrieved from: `type`")
    
    # Numeric
    year: int = Field(ge=1880, le=3000)
    rating: float = Field(ge=0, le=10)
    votes: int = Field(ge=0)
    runtime_mins: float = Field(gt=0, default=None)
    
    # String lists
    genres: CustomTypes.CSVstr = Field(default=None)
    countries: CustomTypes.CSVstr = Field(default=None)
    director: CustomTypes.CSVstr = Field(default=None)
    writer: CustomTypes.CSVstr = Field(default=None)
    composer: CustomTypes.CSVstr = Field(default=None)
    cast: CustomTypes.CSVstr = Field(default=None)
    # cast: CustomTypes.CSVnumsent = Field(default=None)
    
    # Strings
    plot: CustomTypes.CSVnumsent = Field(default=None)
    synopsis: CustomTypes.CSVnumsent = Field(default=None)
    plot_outline: CustomTypes.CSVnumsent = Field(default=None)
    
    # Financial
    budget_mil: float = Field(ge=0, default=None, 
                              description="Strip $/, & text after first space")
    opening_weekend_gross_mil: float = Field(ge=0, default=None)
    cumulative_worldwide_gross_mil: float = Field(ge=0, default=None)
    

# TODO place media/animals/nations models/queries/processors in 
# {media/eco/global}_pulse.py    
# TODO implement 4 pydantic processed data models + 1 valid/invalid demo

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



# XXX Scratch tests
valid_obj = {}
invalid_obj = {}
pd.DataFrame(pd.json_normalize(dict(valid_obj)))
pd.DataFrame(pd.json_normalize(dict(invalid_obj)))

# try: IMDbFilm(**valid_obj)  
# except ValidationError as e: pprint.pp(e.errors())
# try: IMDbFilm(**invalid_obj)  
# except ValidationError as e: pprint.pp(e.errors())



# --------------------------
# --- Metadata retrieval ---
# --------------------------

# Subclass Processor

# TODO move these to media_pulse
# TODO implement 5 subclasses

class IMDbFilmProcessor(BaseProcessor):    
    def retrieve(self):
        # title = self.query.title
        
        # Retrieval routine
        
        obj = []
        self.obj = obj
        return self
    
    def process(self):
        # Processing routine
        
        data = []
        self.data = data
        return self



# XXX Scratch tests
# IMDbFilm = []; Film = []
# film = IMDbFilmProcessor(model=IMDbFilm, query=Film)
# film.retrieve().process().to_df()


if __name__ == "__main__":    
    # Comment out (2) to run all tests in script; (1) to run specific tests
    # doctest.testmod(verbose=True)
    doctest_function(IMDbFilm, globs=globals(), verbose=False)
                
    ## One-off tests
    pass
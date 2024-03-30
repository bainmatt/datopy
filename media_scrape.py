""" _summary_
"""

import requests
import textwrap
from typing import List
import pandas as pd

import wptools
from imdb import Cinemagoer
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from display_dataset import display

# -----------------
# --- Wikipedia ---
# -----------------
### Get Wiki 
# (wiki_extract_film_metadata, wiki_extract_novel_metadata, wiki_extract_album_metadata)

# XXX wiki scratch
# page = 'Canada'
# wiki_info = wptools.page(page).get_parse().data['infobox']
# wiki_info['Gini']

# ---------------
# --- Spotify ---
# ---------------
### Get Spotify

# ------------
# --- IMdB ---
# ------------
### Get IMdB
def get_imdb_id(movie_title: str) -> str:
    """ _summary_

    Parameters
    ----------
    movie_title : str
        _description_

    Returns
    -------
    imdb_id : _type_
        _description_
        
    Examples
    --------
    >>> movie_title = "the shawshank redemption"
    >>> tt_id = get_imdb_id(movie_title)
    >>> tt_id
    'tt0111161'

    >>> movie_title = "ths shukshank redumption"
    >>> tt_id = get_imdb_id(movie_title)
    >>> tt_id
    "No IMDb Identifier found for 'ths shukshank redumption'"
    
    """
    
    base_url = "https://www.imdb.com"
    search_url = f"{base_url}/find?q={movie_title}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        search_response = requests.get(search_url, headers=headers)
        search_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    
    soup = BeautifulSoup(search_response.content, 'html.parser')
    result_links = soup.find_all('a', href=True)

    for link in result_links:
        # Return first link containing ttid
        if '/title/tt' in link['href']:
            imdb_id = link['href'].split('/title/')[1].split('/')[0]
            return imdb_id

    # If no links contain ttid
    return f"No IMDb Identifier found for '{movie_title}'"

def get_imdb_reviews(movie_id: str, num_reviews: int = 5) -> List[str]:
    r""" _summary_

    Parameters
    ----------
    movie_id : str
        _description_
    num_reviews : int, default=5
        _description_

    Returns
    -------
    reviews : _type_
        _description_
        
    Examples
    --------
    >>> movie_title = "finding nemo"
    >>> movie_id = get_imdb_id(movie_title)
    >>> movie_reviews = get_imdb_reviews(movie_id, num_reviews=2)
    >>> for i, review in enumerate(movie_reviews, start=1):
    ...     print(f"Review {i}:\n{textwrap.fill(review[:50], 79)} ... \n");
    Review 1:
    I'll be totally honest and confirm to you that eve ... 
    <BLANKLINE>
    Review 2:
    I have enjoyed most of the computer-animated films ... 
    <BLANKLINE>
    """
    
    base_url = f"https://www.imdb.com/title/{movie_id}/reviews"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        review_containers = soup.find_all('div', 
                                          class_='text show-more__control')

        reviews = []
        for review_container in review_containers[:num_reviews]:
            review_text = review_container.text.strip()
            reviews.append(review_text)

        return reviews
    else:
        print(f"Failed to retrieve reviews. Status code: {response.status_code}")
        return None

# TODO clean up field extraction and add error-handling; example output LIMIT
def get_film_metadata(movie_title):
    """_summary_

    Parameters
    ----------
    movie_title : _type_
        _description_

    Returns
    -------
    {result} : _type_
        _description_
        
    Examples
    --------
    >>> title = 'Promising young woman'
    >>> movie_df = get_film_metadata(title)
    >>> movie_df
              Title   imdbID  ...                                               Plot                                           Synopsis
    0  Finding Nemo  0266543  ...  After his son is captured in the Great Barrier...  Two clownfish, Marlin (Albert Brooks) and his ...
    <BLANKLINE>
    [1 rows x 15 columns]
    
    """
    
    # ', '.join(writer['name'] if (movie['writer'] and 
    #           'name' in writer.keys()) else None
    #           for writer in movie['writer']),
    
    
    # Create an IMDb object
    ia = Cinemagoer()

    # Search for the movie by title
    movies = ia.search_movie(movie_title)

    if movies:
        # Get the first movie (assumed to be the correct one)
        movie = ia.get_movie(movies[0].movieID)

        # Extract movie attributes
        movie_data = {
            "Title": movie['title'],
            "imdbID": movie['imdbID'],
            "Type": movie['kind'],
            "Year": movie['year'],
            "Genres": ', '.join(movie['genres']),
            "Countries": ', '.join(movie['countries']),
            "Runtimes": ', '.join(str(runtime) 
                                  for runtime in movie['runtimes']) +  "minutes",
            # "Directors": ', '.join(director['name'] 
            #                        for director in movie['director']),
            # "Writers": ', '.join(writer['name'] 
            #                      if movie['writer']
            #                      else None
            #                      for writer in movie['writer']),
            # "Composers": ', '.join(composer['name'] 
            #                        for composer in movie['composer']),
            "Cast": ', '.join(actor['name'] for actor in movie['cast']),
            "Rating": movie['rating'],
            "Votes": movie['votes'],
            "Plot Outline": movie['plot outline'],
            "Plot": movie['plot'][0],
            "Synopsis": movie['synopsis'][0],
        }

        # Create a DataFrame
        df = pd.DataFrame([movie_data])
        return df
    else:
        print(f"{movie_title} not found.")
        return None

# XXX get_film_metadata scratch
# title = 'Finding nemo'
# movie_df = get_film_metadata(title)
# display("movie_df").r(globals())

if __name__ == "__main__":
    import doctest
    from nb_utils import doctest_function
        
    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod()
    # doctest_function(get_film_metadata, globs=globals())
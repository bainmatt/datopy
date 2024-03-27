""" _summary_
"""

import requests
import textwrap
from typing import List
import pandas as pd

# import wptools
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from imdb import Cinemagoer
from bs4 import BeautifulSoup

# -----------------
# --- Wikipedia ---
# -----------------
### Get Wiki 
# (wiki_extract_film_metadata, wiki_extract_novel_metadata, wiki_extract_album_metadata)

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


# TODO
def get_film_metadata(title):
    # Create an IMDb object
    ia = Cinemagoer()

    # Search for the movie by title
    movies = ia.search_movie(title)

    if movies:
        # Get the first movie (assumed to be the correct one)
        movie = ia.get_movie(movies[0].movieID)

        # Extract movie attributes
        movie_data = {
            "Title": movie['title'],
            "Year": movie['year'],
            "Genres": ', '.join(movie['genres']),
            "Plot Outline": movie['plot outline'],
            "Cast": ', '.join(actor['name'] for actor in movie['cast']),
            "Directors": ', '.join(director['name'] for director in movie['directors']),
            "Rating": movie['rating'],
            "Votes": movie['votes'],
            "Runtimes": ', '.join(str(runtime) for runtime in movie['runtimes']) + " minutes"
        }

        # Create a DataFrame
        df = pd.DataFrame([movie_data])

        # Print DataFrame
        df

        # Return DataFrame if needed
        return df
    else:
        print("Movie not found.")
        return None

title = 'Promising Young Woman'
movie_df = get_film_metadata(title)
movie_df

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# ---------------
# --- SCRATCH ---
# ---------------
class test():
    def __init__(self, x):
        self.x = x
        return None
        
    def method(self, y):
        return self.x + y

from display_dataset import make_df
df1 = make_df('AB', [1, 2]); df2 = make_df('AB', [3, 4])
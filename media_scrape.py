""" _summary_
"""

import requests
from bs4 import BeautifulSoup

# ---------------
# --- Spotify ---
# ---------------
### Get Spotify

# ------------
# --- IMdB ---
# ------------
### Get IMdB
def get_imdb_id(movie_title):
    """ _summary_

    Parameters
    ----------
        movie_title : _type_
            _description_

    Returns
    -------
        imdb_id : _type_
            _description_
        
    Examples
    --------
    >>> movie_title = "The_Shawshank_Redemption"
    >>> tt_id = get_imdb_id(movie_title)
    >>> if tt_id: print(f"IMDb Identifier (ttID) for '{movie_title}': {tt_id}")
    ... else: print(f"No IMDb Identifier found for '{movie_title}'.")
    IMDb Identifier (ttID) for 'The_Shawshank_Redemption': 0111161

    >>> movie_title = "The_Shuwshank_Redumption"
    >>> tt_id = get_imdb_id(movie_title)
    >>> if tt_id: print(f"IMDb Identifier (ttID) for '{movie_title}': {tt_id}")
    ... else: print(f"No IMDb Identifier found for '{movie_title}'.")
    No IMDb Identifier found for 'The_Shuwshank_Redumption'.
    
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
        if '/title/tt' in link['href']:
            imdb_id = link['href'].split('/title/tt')[1].split('/')[0]
            return imdb_id

    return None

class test():
    def __init__(self, x):
        self.x = x
        return None
    
    def method(self, y):
        return self.x + y

# -----------------
# --- Wikipedia ---
# -----------------
### Get Wiki
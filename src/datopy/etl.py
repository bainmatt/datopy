"""
Tools for efficient web-based data retrieval, data processing,
table creation, and populating empty metadata fields.

.. note:: WIP.

Overview
~~~~~~~~

.. currentmodule:: datopy.etl

.. rubric:: Extract

Utilities for data retrieval.

.. autosummary::
    :nosignatures:

.. rubric:: Transform

Basic data processing and transformation of raw data.

.. autosummary::
    :nosignatures:

    omit_string_patterns

.. rubric:: Load

Utilities related to finding and loading data into a database.

.. autosummary::
    :nosignatures:

    retrieve_wiki_topics

API
~~~
"""

import re
import sys
import pprint
import doctest
import wptools

from datopy.workflow import doctest_function
from datopy.util._numpydoc_validate import numpydoc_validate_module


# -- Extract -----------------------------------------------------------------


# -- Transform ---------------------------------------------------------------


def omit_string_patterns(input_string: str, patterns: list[str]) -> str:
    r"""
    Prune multiple character patterns from a string.

    Parameters
    ----------
    input_string : str
        The to-be-cleaned string.

    patterns : list[str]
        A list of patterns to omit from the string.

    Returns
    -------
    str
        The input string with the supplied patterns ommitted.

    Examples
    --------
    >>> from datopy.etl import omit_string_patterns

    >>> input_string = "[[A \\\\ messy * string * with undesirable /patterns]]"
    >>> patterns_to_omit = ["[[", "]]", "* ", "\\\\ ", "/", "messy ", "un" ]
    >>> output_string = omit_string_patterns(input_string, patterns_to_omit)
    >>> print(output_string)
    A string with desirable patterns
    """
    pattern = '|'.join(re.escape(p) for p in patterns)
    return re.sub(pattern, '', input_string)


# -- Load --------------------------------------------------------------------


# -- Topic retrieval ---------------------------------------------------------


# TODO: take first and last entry (relative indices non-0'ed))

def retrieve_wiki_topics(listing_page: str, verbose: bool = True) -> list[str]:
    """
    Compile a list of related topics by scraping a Wikipedia page.

    Parameters
    ----------
    listing_page : str
        The title of a Wikipedia article containing topics to be retrieved.
    verbose : bool, default=True
        Option to enable/disable printouts.

    Returns
    -------
    list[str]
        A list of topics (by article name) extracted from the listing page.

    Notes
    -----
    Only hyperlinked topics (those with a Wikipedia page) are retrieved.
    Search Wikipedia's catalogue of listing pages here:
    https://en.wikipedia.org/wiki/List_of_lists_of_lists
    """

    wiki_parse = wptools.page(listing_page).get_parse().data['parsetree']

    regex_pattern = re.compile(r"\[\[(.*?)\]\]")
    matches = regex_pattern.findall(wiki_parse)
    pages = [match.split('|')[0].strip() for match in matches]
    target_pages = pages[4:-3]

    if verbose:
        pprint.pp(target_pages)

    return target_pages


if __name__ == "__main__":
    # Comment out (2) to run all tests in script; (1) to run specific tests
    # doctest.testmod(verbose=True)
    # doctest_function(get_film_metadata, globs=globals())

    numpydoc_validate_module(sys.modules['__main__'])

    # One-off tests
    # listing_page = "List of legendary creatures from China"
    # retrieve_wiki_topics(listing_page)

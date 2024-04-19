"""
The :mod:`datatools` module includes utilities for managing data I/O,
data modelling, ETL pipelines, and utilities for testing, inspecting data,
and styling matplotlib plots.
"""

from datatools.workflow_utils import doctest_function, git_module_loader
from datatools.datamodel_utils import (
    apply_recursive,
    compare_dict_keys,
    list_to_dict,
    schema_jsonify,
)
from datatools.etl_utils import (
    omit_string_patterns,
    retrieve_wiki_topics,
)
from datatools.display_dataset import display, make_df
from datatools.stylesheet import (
    customize_matplotlib_rcParams,
    suppress_output
)
from datatools.run_doctests import run_doctest_suite
from datatools._examples import *
from datatools._media_scrape import *

__all__ = [
    "doctest_function",
    "git_module_loader",
]

"""
Configuration file for the Sphinx documentation builder.

Full list of built-in configuration values:
https://www.sphinx-doc.org/en/master/usage/configuration.html

Full list of configuration values for autodoc:
https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

Quickstart:
https://www.sphinx-doc.org/en/master/tutorial/getting-started.html

A nice succinct guide:
https://hplgit.github.io/teamods/sphinx_api/html/sphinx_api.html

Theming references:
https://sphinx-themes.org/
https://sphinx-themes.org/sample-sites/furo/
https://pydata-sphinx-theme.readthedocs.io/en/stable/
https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html

Nice model projects:
*https://python.arviz.org/en/stable/index.html
*https://tox.wiki/en/latest/index.html
https://github.com/scikit-learn/scikit-learn/blob/main/doc/conf.py
https://github.com/gbif/pygbif/tree/master

Beautiful docs (at the cost of total automation):
https://mkdocstrings.github.io/python/usage/

rst reference:
https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#substitution-definitions
https://bashtage.github.io/sphinx-material/rst-cheatsheet/rst-cheatsheet.html

For additional numpy-style doctest functionality:
https://pypi.org/project/pytest-doctestplus/

Sphinx build configuration:
https://sphinx-rtd-trial.readthedocs.io/en/1.1.3/invocation.html

Handy recipes:
$ make doctest -B  # overwrite previous build

"""

# --- Variables and paths ---

# For auto-generating documentation from docstrings
import os
import sys
import pathlib

sys.path.insert(0, os.path.abspath('../src'))


# --- Doctest conditional skipping option ---
# Conditionally skip computationally intensive examples
# https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html

doctest_global_setup = '''
try:
    import pandas as pd
except ImportError:
    pd = None

skip_slow = True
'''


# --- Project information ---
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import pkg_resources
version = pkg_resources.get_distribution('datopy').version

project = 'datopy'
copyright = '2024, Matthew Bain'
author = 'Matthew Bain'
release = version


# --- General configuration ---
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Doctest:
# https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html#confval-doctest_test_doctest_blocks

# Autodocs/autosummary:
# https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#directive-autosummary

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "matplotlib.sphinxext.plot_directive",
    "matplotlib.sphinxext.mathmpl",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.todo",
]


# --- Customize autosummary options ---
# https://autodocsumm.readthedocs.io/en/latest/conf_settings.html

autodoc_default_options = {
    # Show all objects within a module on one page via embedded TOC
    # NOTE: required for autodoc_pydantic so that models aren't orphaned
    # NOTE: turn off for a more manageable (albeit less comprehensive) toc tree
    # ... but change `show_toc_level` from 1 to 2 so members are accessible
    # ... and turn off `autodoc_pydantic` so pydantic models aren't orphaned
    # ... and turn on `numpydoc_class_members_toctree` so members not orphaned

    "members": True,
    # Don't document private, inherited, or special class members
    "private-members": False,
    "inherited-members": False,
    "special-members": False,
    # "special-members": "__init__",
    # show name and source of object on which a subclass is based
    "show-inheritance": True,
    "undoc-members": False,
    "member-order": "bysource",
    "exclude-members": "main",
}

todo_include_todos = False
todo_link_only = True


# --- Cusomize intersphinx options ---
# Links to documentation for any base types that Sphinx should source and
# hyperlink within the rendered definitions.
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#module-sphinx.ext.intersphinx

intersphinx_mapping = {
    "python": ("https://docs.python.org/{.major}".format(sys.version_info), None),
    "numpy": ("https://numpy.org/doc/stable", None),
    # "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "matplotlib": ("https://matplotlib.org/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    # "joblib": ("https://joblib.readthedocs.io/en/latest/", None),
    # "seaborn": ("https://seaborn.pydata.org/", None),
    # "skops": ("https://skops.readthedocs.io/en/stable/", None),
    # "scikit-learn": ("https://scikit-learn.org/stable/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "datopy": ("https://datopy.readthedocs.io/stable/", None),
}


# --- Customize matplotlib.sphinxext.plot_directive options ---
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html

# This extension is used for doctest plots and output rendered inline
plot_formats = ["svg"]
plot_include_source = True
plot_html_show_formats = False
plot_html_show_source_link = False


# --- Customize autodoc_pydantic options ---
# https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html

# NOTE: auto_pydantic does not play well with TOC or `make clean` after build!!
# https://github.com/mansenfranzen/autodoc_pydantic/issues/33

autodoc_pydantic_model_show_config_summary = True
# don't include summary table for fields (config summary is sufficient)
autodoc_pydantic_model_show_field_summary = True

autodoc_pydantic_model_show_json = True
# autodoc_pydantic_model_show_erdantic_figure_collapsed = True
# autodoc_pydantic_model_show_schema_json = True

autodoc_pydantic_model_show_members = True
autodoc_pydantic_field_show_required = True
autodoc_pydantic_field_show_optional = True
autodoc_pydantic_field_show_default = True
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_field_show_alias = True

# below a validator list the fields to which it is applied (redundant)
autodoc_pydantic_validator_list_fields = False
# below a field list the validator(s) applied to it
autodoc_pydantic_field_list_validators = True
# True overrides default object signature with a more informative version
autodoc_pydantic_validator_replace_signature = True
autodoc_pydantic_settings_show_validator_summary = True
autodoc_pydantic_settings_show_validator_members = True
autodoc_pydantic_settings_hide_reused_validator = False

autodoc_pydantic_model_member_order = "bysource"
autodoc_pydantic_model_summary_list_order = "bysource"
autodoc_pydantic_settings_member_order = "bysource"
autodoc_pydantic_settings_summary_list_order = "bysource"


# --- Customize Napoleon options ---
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

# napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = True
# ?for footnote compatibility
napoleon_use_admonition_for_references = True
# ?place parameter description below its definition
napoleon_use_ivar = False
# napoleon_use_keyword = True
# set to True for a separate ReturnType field
napoleon_use_rtype = True
# turn off parameter list hyperlinks since already available in docstring
napoleon_use_param = False
# turn off sloppy styling of parameter types
napoleon_preprocess_types = False
napoleon_type_aliases = None
# include attribute summary lists within classes where provided
napoleon_attr_annotations = True


# --- Customize numpydocs options ---
# https://numpydoc.readthedocs.io/en/latest/install.html

numpydoc_use_plots = True
# include class methods/attributes summary table
numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = False
# don't clutter left-hand section navigation bar
numpydoc_class_members_toctree = False

# Numpy docstring validation checks
# https://numpydoc.readthedocs.io/en/latest/validation.html

# Report warnings for all validation checks except GL01, GL02, etc.
numpydoc_validation_checks = {
    "all",
    # styling
    "GL01", "GL02", "GL05", "GL08",
    # missing sections
    "ES01", "SA01", "EX01", "RT01",
    # missing elements (period in summary, parameters)
    # NOTE: this should not be used permanently
    "PR01", "SS03",
}

# Objects to exclude from autosummary
templates_path = ['_templates']
exclude_patterns = ['_[!_]*.py', 'main']


# ============================================================================
# Style fine-tuning
# ============================================================================

# --- Options for HTML output ---
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Fundamentals
# html_theme = "alabaster"
# html_theme = "furo"
html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
html_title = "datopy manual"
html_short_title = "datopy"
# html_logo = "_static/datopy-logo.png"
# html_favicon = "_static/datopy-logo.png"

# Fine-tuning
html_context = {
    # TODO check whether the following lines (except the last) are necessary
    "github_url": "https://github.com",  # or your GitHub Enterprise site
    "github_user": "bainmatt",
    "github_repo": "datopy",
    "github_version": "main",
    "doc_path": "docs/source/",
    "default_mode": "light",
}

python_maximum_signature_line_length = 20
math_number_all = True
add_function_parentheses = True
# Show module paths in objects signatures for clarity
add_module_names = True
# Include module/class members in right-hand toc
toc_object_entries = True
# Don't clutter right-hand toc with absolute paths to objects
toc_object_entries_show_parents = "hide"
trim_doctest_flags = True
show_warning_types = True
python_display_short_literal_types = True

# Suppress_warnings = ["WARNING: document isn't included in any toctree"]
# FIXME make this work
suppress_warnings = ["all"]

# If false, no index is generated
html_use_index = False

# Link to underlying rsts
# NOTE: excellent tool for debugging documentation
html_show_sourcelink = True


# --- Sidebar customizations ---

# NOTE: sidebar customization in Furo is limited:
# https://pradyunsg.me/furo/customisation/sidebar/

# Hide sidebar on particular pages where section navigation is empty
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#primary-sidebar-left

html_sidebars = {
    'changelog': [],
    'readme': []
}


# --- Version switcher configuration ---

# Obtain version for version switcher
# References:
# https://github.com/pandas-dev/pandas/blob/main/doc/source/conf.py
# https://github.com/pandas-dev/pandas/blob/main/web/pandas/versions.json

if ".dev" in version:
    switcher_version = "dev"
else:
    # only keep major.minor version number to match versions.json
    # switcher_version = ".".join(version.split(".")[:2])
    switcher_version = version

# TODO check this
# For use with Read the Docs. Reference:
# https://github.com/pydata/pydata-sphinx-theme/blob/main/docs/conf.py
version_match = os.environ.get("READTHEDOCS_VERSION")

# If READTHEDOCS_VERSION doesn't exist, we're not on RTD.
# If it is an integer, we're in a PR build and the version isn't correct.
# If it's "latest" → change to "dev" (what we want the switcher to call it).

if not version_match or version_match.isdigit() or version_match == "latest":
    # For local development, infer the version to match from the package.
    if "dev" in release or "rc" in release:
        switcher_version = "dev"

        # We want to keep the relative reference if we are in dev mode
        # but we want the whole url if we are effectively in a released version
        json_url = "_static/switcher.json"
    else:
        switcher_version = f"v{release}"
elif version_match == "stable":
    switcher_version = f"v{release}"


# --- Additional PyData HTML customizations ---
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#references

html_theme_options = {
    # NOTE: not compatible with Furo. Comment out unless using PyData.
    # Previous/next buttons are unstable in PyData (poor overflow handling)
    "show_prev_next": False,
    "navigation_with_keys": True,

    "show_nav_level": 1,
    # Don't show class methods in right-hand toc by default
    "show_toc_level": 1,

    # "light_logo": "logo-light-mode.png",
    # "dark_logo": "logo-dark-mode.png",

    # TODO ?make this work
    # "content_footer_items": ["last-updated"],

    # Header links
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/header-links.html

    "github_url": "https://github.com/bainmatt/datopy",
    "header_links_before_dropdown": 4,
    # "external_links": [
    #     {
    #         "name": "Website",
    #         "url": "https://bainmatt.github.io/",
    #     },
    # ],
    "icon_links": [
        {
            "name": "Personal website",
            "url": "https://bainmatt.github.io/",
            "icon": "fas fa-link",
            "type": "fontawesome",
        },
    ],
    # "analytics": {"google_analytics_id": "G-XX"},

    # Version switcher dropdowns
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/version-dropdown.html

    # Example additional rtd configurations:
    # https://github.com/pydata/pydata-sphinx-theme/blob/30be4d46fe4845503aacf886af4f5af8581057c2/docs/conf.py

    "switcher": {
        "json_url": "https://bainmatt.github.io/datopy/_static/switcher.json",
        "version_match": switcher_version,
    },
    "show_version_warning_banner": True,
    "navbar_align": "content",
    # "navbar_start": [
    #     "navbar-logo", "version-switcher",
    # ],
    "navbar_end": [
        "version-switcher",
        "theme-switcher", "navbar-icon-links"
    ],
}

# Source buttons
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/source-buttons.html

use_edit_page_button = False

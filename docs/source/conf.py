"""
Configuration file for the Sphinx documentation builder.

Full list of built-in configuration values:
https://www.sphinx-doc.org/en/master/usage/configuration.html

Full list of configuration values for autodoc:
https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

Quickstart:
https://www.sphinx-doc.org/en/master/tutorial/getting-started.html

Theming references:
https://sphinx-themes.org/
https://sphinx-themes.org/sample-sites/furo/
https://pydata-sphinx-theme.readthedocs.io/en/stable/
https://sphinx-themes.org/sample-sites/pydata-sphinx-theme/#

Nice model projects:
*https://tox.wiki/en/latest/index.html
https://github.com/scikit-learn/scikit-learn/blob/main/doc/conf.py
https://github.com/gbif/pygbif/tree/master

Beautiful docs (no auto-doctests):
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

skip_slow = False
'''


# --- Project information ---
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'datopy'
copyright = '2024, Matthew Bain'
author = 'Matthew Bain'
release = '0.0.1'


# --- General configuration ---
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
#
# Doctest:
# https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html#confval-doctest_test_doctest_blocks
#
# Autodocs/autosummary:
# https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#directive-autosummary

extensions = [
   'sphinx.ext.duration',
   'sphinx.ext.doctest',
   'sphinx.ext.autodoc',
   'sphinx.ext.autosummary',
   'sphinx.ext.napoleon',
   'sphinx.ext.coverage',
   'numpydoc',
   'sphinx.ext.intersphinx',
   'matplotlib.sphinxext.plot_directive',
   'matplotlib.sphinxext.mathmpl',
   'sphinxcontrib.autodoc_pydantic',
]


# --- Customize autosummary options ---
# https://autodocsumm.readthedocs.io/en/latest/conf_settings.html

autodoc_default_options = {
   # Show all objects within a module on one page via embedded TOC
   'members': False,
   'private-members': False,
   'inherited-members': False,
   'special-members': False,
   'show-inheritance': True,
   'undoc-members': False,
}


# --- Cusomize intersphinx options ---
# Links to documentation for any base types that Sphinx should source and
# hyperlink within the rendered definitions.
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#module-sphinx.ext.intersphinx

# intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
intersphinx_mapping = {
    "python": ("https://docs.python.org/{.major}".format(sys.version_info), None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "matplotlib": ("https://matplotlib.org/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "joblib": ("https://joblib.readthedocs.io/en/latest/", None),
    "seaborn": ("https://seaborn.pydata.org/", None),
    "skops": ("https://skops.readthedocs.io/en/stable/", None),
    "scikit-learn": ("https://scikit-learn.org/stable/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    # "datopy": {"https://bainmatt.github.io/datopy/", None},
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
# NOTE auto_pydantic does not play well with TOC or `make clean` after build!!
# https://github.com/mansenfranzen/autodoc_pydantic/issues/33

autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_model_show_members = False
# autodoc_pydantic_field_show_required = True
# autodoc_pydantic_field_show_optional = True
autodoc_pydantic_settings_hide_reused_validator = True
autodoc_pydantic_settings_show_validator_members = False

# autodoc_pydantic_model_signature_prefix = 'pydantic model'
# autodoc_pydantic_model_show_erdantic_figure_collapsed = True
# autodoc_pydantic_model_show_schema_json = True


# --- Customize Napoleon options ---
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

# napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True  # ?for footnote compatibility
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = False


# --- Customize numpydocs options ---
# https://numpydoc.readthedocs.io/en/latest/install.html

numpydoc_use_plots = True
numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = True

# Numpy docstring validation checks
# https://numpydoc.readthedocs.io/en/latest/validation.html
# 
# Report warnings for all validation checks except GL01, GL02, and GL05
numpydoc_validation_checks = {"GL01", "GL02", "GL05"}  # "all"

# FIXME fix this to actually exclude the specified patterns
templates_path = ['_templates']
# exclude_patterns = []
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
# html_title = "datopy: Data tools for Python"
html_short_title = "datopy"
# html_logo = "_static/datopy-logo.png"
# html_favicon = "_static/datopy-logo.png"

# Fine-tuning
html_theme_options = {
    "navigation_with_keys": True,
    # "light_logo": "logo-light-mode.png",
    # "dark_logo": "logo-dark-mode.png",
}

python_maximum_signature_line_length = 20
math_number_all = True
add_function_parentheses = True
add_module_names = False
toc_object_entries = True
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
html_show_sourcelink = False

# Exclude parent paths from appearing in TOC
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_sidebars
# 
# NOTE sidebar customization in Furo is limited:
# https://pradyunsg.me/furo/customisation/sidebar/
# 
# html_sidebars = {
#    '**': ["globaltoc.html"],
# }


# --- Additional PyData HTML customizations ---
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#references

# NOTE not compatible with Furo. Comment out unless using PyData.
html_theme_options = {
    # Previous/next buttons are unstable in PyData (poor overflow handling)
    "show_prev_next": False,
    "show_nav_level": 1,
    # Show class methods in right-hand toc by default
    "show_toc_level": 2,
}

# html_context = {
#     "github_url": "https://github.com", # or your GitHub Enterprise site
#     "github_user": "bainmatt",
#     "github_repo": "datopy",
#     "github_version": "main",
#     "doc_path": "docs/source",
# }

# Source buttons
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/source-buttons.html
use_edit_page_button = False
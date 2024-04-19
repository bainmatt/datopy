"""
Configuration file for the Sphinx documentation builder.

Full list of built-in configuration values:
https://www.sphinx-doc.org/en/master/usage/configuration.html

Quickstart:
https://www.sphinx-doc.org/en/master/tutorial/getting-started.html

Style references: 
https://sphinx-themes.org/
https://sphinx-themes.org/sample-sites/furo/
https://pydata-sphinx-theme.readthedocs.io/en/stable/
https://sphinx-themes.org/sample-sites/pydata-sphinx-theme/#

Nice model project:
https://github.com/gbif/pygbif/tree/master
"""

# --- Variables and paths ---
# For auto-generating documentation from docstrings
import os
import sys
import pathlib

# sys.path.insert(0, pathlib.Path(__file__).parents[2].
#                 joinpath('src/datatools').resolve().as_posix())
sys.path.insert(0, os.path.abspath('../src'))


# --- Project information ---
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'datatools'
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
]

# --- Napoleon settings for autodocs ---
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

# napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# --- Numpy-style docstring settings for autodocs ---
# https://numpydoc.readthedocs.io/en/latest/install.html
numpydoc_use_plots = True
numpydoc_show_inherited_class_members = False

# Numpy docstring validation checks
# https://numpydoc.readthedocs.io/en/latest/validation.html#validation-checks
# https://numpydoc.readthedocs.io/en/latest/validation.html
# Report warnings for all validation checks except GL01, GL02, and GL05
numpydoc_validation_checks = {"all", "GL01", "GL02", "GL05"}


templates_path = ['_templates']
exclude_patterns = []


# ============================================================================
# Style fine-tuning
# ============================================================================

# --- Options for HTML output ---
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'furo'
html_static_path = ['_static']

# [MB] added
# sticky_navigation = True

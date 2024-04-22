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

Nice model project:
https://github.com/gbif/pygbif/tree/master

Beautiful docs (no auto-doctests):
https://mkdocstrings.github.io/python/usage/

Sphinx build configuration:
https://sphinx-rtd-trial.readthedocs.io/en/1.1.3/invocation.html

Numpydocs doctest skipping:
https://pypi.org/project/pytest-doctestplus/

Handy:
$ make doctest -B  # overwrite previous build

"""

# --- Variables and paths ---
# For auto-generating documentation from docstrings
import os
import sys
import pathlib

# sys.path.insert(0, pathlib.Path(__file__).parents[2].
#                 joinpath('src/datopy').resolve().as_posix())
sys.path.insert(0, os.path.abspath('../src'))


# --- Doctest conditional skipping option ---
# Conditionally skip computationally intensive examples
# TODO configure this
skip_slow = True


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
   # 'matplotlib.sphinxext',
   # 'matplotlib.sphinxext.mathmpl',
   # 'matplotlib.sphinxext.only_directives',
   # 'matplotlib.sphinxext.plot_directive',
   # 'autodoc_pydantic',
]


# --- Custom options for autosummary ---
# https://autodocsumm.readthedocs.io/en/latest/conf_settings.html
autodoc_default_options = {
   # Show all objects within a module on one page via embedded TOC
   # 'members': True,
   'private-members': False,
   'inherited-members': False,
   'special-members': False,
}

add_function_parentheses = True
add_module_names = False
toc_object_entries = True
toc_object_entries_show_parents = 'hide'
trim_doctest_flags = True
show_warning_types = False
suppress_warnings = ['all']
# suppress_warnings = ["WARNING: document isn't included in any toctree"]
# exclude_patterns = ['_[!_]*.py', 'main']
python_display_short_literal_types = True


# --- Options for auto-generated Pydantic visualizations ---
# https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html
# autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_show_members = True
# autodoc_pydantic_model_show_erdantic_figure_collapsed = True
# autodoc_pydantic_model_show_schema_json = True


# --- Napoleon settings for autodocs ---
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

# napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = True
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
numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = True

# Numpy docstring validation checks
# https://numpydoc.readthedocs.io/en/latest/validation.html#validation-checks
# https://numpydoc.readthedocs.io/en/latest/validation.html
# Report warnings for all validation checks except GL01, GL02, and GL05
numpydoc_validation_checks = {"GL01", "GL02", "GL05"}  # "all"


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


# This is the expected signature of the handler for this event, cf doc
def autodoc_skip_member_handler(app, what, name, obj, skip, options):
    # Basic approach; you might want a regex instead
    return name.startswith("main")

# Automatically called by sphinx at startup
def setup(app):
    # Connect the autodoc-skip-member event from apidoc to the callback
    app.connect('autodoc-skip-member', autodoc_skip_member_handler)

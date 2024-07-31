..
   Sphinx reST guide:
   https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
   Directives:
   https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
   Admonitions:
   https://documatt.com/restructuredtext-reference/admonitions.html

.. _quickstart:

datopy
======

.. image:: https://github.com/bainmatt/datopy/actions/workflows/tests.yml/badge.svg
   :alt: CI
.. image:: https://readthedocs.org/projects/datopy/badge/?version=latest
   :target: https://datopy.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

----

**datopy** (da-toh-pie) is a Python library for people who
work with unstructured data, providing a simple workflow for
building data models and ETL (extract, transform, load) pipelines.

----

This package also includes utilities for:

- Data retrieval (web scraping and API-based data retrieval)
- Input/output processes (loading and inspecting data)
- Jupyter Notebook workflows

.. note::

   This project is under active development.

Getting Started
---------------

.. _installation:

Installation
~~~~~~~~~~~~

To use datopy, first install it using pip:

.. code-block:: console

   $ pip install "git+https://github.com/bainmatt/datopy.git#egg=datopy"

Cloning
~~~~~~~

Step 1. Clone the repo:

.. code-block:: console

   $ git clone https://github.com/bainmatt/datopy.git
   $ cd datopy

Step 2. Install dependencies:

.. code-block:: console

   $ conda env create -f environment.yml
   $ conda activate datopy

Development
~~~~~~~~~~~

.. admonition:: WIP.
   :class: note

   Instructions on typing/testing/documentation, CI/CD, and
   conventions for developers.

.. A representative use case for each module.
.. _usage:

Usage
-----

..
   Cross reference auto-generated docs for a function
   Replace `func` with `mod` for a module and `meth` for a method
   https://www.sphinx-doc.org/en/master/usage/domains/python.html#cross-referencing-python-objects

Dataset inspection
~~~~~~~~~~~~~~~~~~

*API reference*: :mod:`datopy.inspection`

Produce multiple parallel, informative displays of Pandas data frames and
NumPy arrays for data exploration and inspection.


..
   .. Use a custom admonition

   .. admonition:: Example
      :class: tip

.. code-block:: python

   >>> import numpy as np
   >>> import pandas as pd
   >>> from datopy.inspection import display, make_df

   >>> df1 = make_df('AB', [1, 2]); df2 = make_df('AB', [3, 4])
   >>> display('df1', 'df2', 'pd.concat([df1, df2])', globs=globals(), bold=False)

   df1
   --- (2, 2) ---
      A   B
   1  A1  B1
   2  A2  B2


   df2
   --- (2, 2) ---
      A   B
   3  A3  B3
   4  A4  B4


   pd.concat([df1, df2])
   --- (4, 2) ---
      A   B
   1  A1  B1
   2  A2  B2
   3  A3  B3
   4  A4  B4


Metadata scraping
~~~~~~~~~~~~~~~~~

*API reference*: :mod:`datopy._media_scrape`

.. admonition:: WIP.
   :class: note
   
   More usage examples to come.

Retrieve media-related data from Spotify, IMDb, and Wikipedia.


Acknowledgements
----------------

This package is powered by:

   - `mypy <https://mypy.readthedocs.io/en/stable/index.html>`_ type checking
   - `pytest <https://docs.pytest.org/en/8.0.x/contents.html>`_ unit testing
   - `Flake8 <https://flake8.pycqa.org/en/latest/index.html>`_ linting
   - `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_ documentation
   - `numpydoc <https://numpydoc.readthedocs.io/en/latest/index.html>`_ docstrings
   - `PyData <https://pydata-sphinx-theme.readthedocs.io/en/stable/>`_ theming
   - `Read the Docs <https://readthedocs.org/>`_ hosting
   - `GitHub Actions <https://docs.github.com/en/actions>`_ continuous integration
   - `PyPI <https://pypi.org/>`_ packaging
   - `Pydantic <https://docs.pydantic.dev/latest/>`_ data validation


License
-------

This project is licensed under the MIT License.


Contact
-------

Project Link: https://github.com/bainmatt/datopy

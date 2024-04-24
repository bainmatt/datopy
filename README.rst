.. 
   Sphinx reST guide:
   https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
   Directives:
   https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
   Admonitions:
   https://documatt.com/restructuredtext-reference/admonitions.html


datopy: Python tools for data
=============================

Python tools for data retrieval, I/O, and Jupyter notebook workflows.

.. note::

   This project is under active development.


Getting Started
---------------

.. Anchor for cross-referencing
.. _installation:

Installation
~~~~~~~~~~~~

To use data-tools, first install it using pip:

.. code-block:: console

   (.venv) $ pip install "git+https://github.com/bainmatt/data-tools.git#egg=datopy"

Cloning
~~~~~~~

1. Clone the repo::

   $ git clone https://github.com/bainmatt/datopy.git
   $ cd datopy

2. Install dependencies::

   $ conda env create -f environment.yml
   $ conda activate dato-py

Development
~~~~~~~~~~~

TODO add this section

.. 
   Downloading a particular module
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Inside a notebook, run the following cell to import a module of interest.::

      # 1. Import urllib
      import urllib.request

      # 2. Set URL of the module to import
      module_url = "https://raw.githubusercontent.com/<user>/data-tools/main/module.py"

      # 3. Download the module
      urllib.request.urlretrieve(module_url, "module.py")

      # 4. Import the module
      import module

   Now you can use functions from the module::

      module.function(args)


.. A representative use case for each module.
.. _usage:

Usage
-----

.. 
   Cross reference auto-generated docs for a function
   Replace `func` with `mod` for a module and `meth` for a method
   https://www.sphinx-doc.org/en/master/usage/domains/python.html#cross-referencing-python-objects

Dataset inspection (:mod:`datopy.inspection`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO finish this section

Produce multiple parallel, informative displays of Pandas data frames and 
NumPy arrays for data exploration and inspection.

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


   .. 
      .. literalinclude:: datopy/datopy.inspection.display.rst
      .. include:: datopy/datopy.inspection.display.rst


**x**: Use `nb_utils.py` to save your Colab environment files to your mounted Google Drive from within a Colab notebook.


**Media scraping**: Use `media_scrape.py` to scrape media-related data from Spotify, IMDb, and Wikipedia.


Roadmap
-------

- [ ] Roll out first stable release


License
-------

This project is licensed under the MIT License.


Contact
-------

Project Link: https://github.com/bainmatt/datopy

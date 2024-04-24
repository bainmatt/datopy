.. data-tools documentation master file, created by
   sphinx-quickstart on Thu Apr 18 15:11:25 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. TOC tree options:
   https://sphinx-doc-zh.readthedocs.io/en/latest/markup/toctree.html

datopy
======

.. Home page intro text

**datopy** (day-toh-pie) is a Python library for people who 
work with data that aims to simplify repetitive data modelling tasks and
routine ETL workflows.

.. Use :doc: to reference a document rather than a section within it

Check out the :ref:`Usage <usage>` section for further information, including how to :ref:`install <installation>` the project.

.. note::

   This project is under active development.

.. Main left-hand navbar TOC

.. toctree::
   :maxdepth: 3
   :caption: Contents:


Indices and tables
==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


.. Home page TOC

Contents
--------

.. toctree::
   :maxdepth: 2

   readme
   api
   api_models
   changelog

   .. usage

.. 
   An additional hidden TOC tree containing all pages (below max depth)
   to supress the "WARNING: document isn't included in any toctree".

   .. toctree::
      :hidden:
      :maxdepth: 10
      :glob:

      *

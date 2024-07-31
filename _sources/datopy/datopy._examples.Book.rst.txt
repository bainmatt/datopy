.. Reference: https://stackoverflow.com/questions/48074094/use-sphinx-autosummary-recursively-to-generate-api-documentation

datopy.\_examples.Book
======================

.. currentmodule:: datopy._examples

.. autoclass:: Book

   
   

   .. HACK -- the point here is that we don't want this to appear in the output, but the autosummary should still generate the pages.

   
      .. autosummary::
         :toctree:
      
         Book.artist
         Book.title
   
   

   
      .. autosummary::
         :toctree:
      
         Book.count
         Book.index
   
   
.. Reference: https://stackoverflow.com/questions/48074094/use-sphinx-autosummary-recursively-to-generate-api-documentation

datopy.\_examples.Album
=======================

.. currentmodule:: datopy._examples

.. autoclass:: Album

   
   

   .. HACK -- the point here is that we don't want this to appear in the output, but the autosummary should still generate the pages.

   
      .. autosummary::
         :toctree:
      
         Album.artist
         Album.title
   
   

   
      .. autosummary::
         :toctree:
      
         Album.count
         Album.index
   
   
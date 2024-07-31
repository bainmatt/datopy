.. Reference: https://stackoverflow.com/questions/48074094/use-sphinx-autosummary-recursively-to-generate-api-documentation

datopy.\_examples.Film
======================

.. currentmodule:: datopy._examples

.. autoclass:: Film

   
   

   .. HACK -- the point here is that we don't want this to appear in the output, but the autosummary should still generate the pages.

   
      .. autosummary::
         :toctree:
      
         Film.artist
         Film.title
   
   

   
      .. autosummary::
         :toctree:
      
         Film.count
         Film.index
   
   
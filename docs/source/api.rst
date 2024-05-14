.. 
    List all modules containing docstrings from which to construct the docs.
    
    To run and compile doctests:
    
        (docs) $ make doctest
        
    To build docs:
    
        (docs) $ make html
        
    To clean build directory for a fresh start:
    
        (docs) $ make clean


Core API
========

.. rubric:: Modules

..
    .. autosummary::
    :toctree: generated

    datopy

.. autosummary::
    :toctree: datopy
    :recursive:
    
    datopy.inspection
    datopy.workflow
    datopy.modeling
    datopy.etl
    datopy.stylesheet
    datopy.run_doctests
    datopy.update_reqs
    datopy._examples
    datopy._media_scrape

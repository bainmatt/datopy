.. 
    List all modules containing docstrings from which to construct the docs.
    
    To run and compile doctests:
    
        (docs) $ make doctest
        
    To build docs:
    
        (docs) $ make html
        
    To clean build directory for a fresh start:
    
        (docs) $ make clean


API
===

.. rubric:: Modules

..
    .. autosummary::
    :toctree: generated

    datatools

.. autosummary::
    :toctree: datatools
    :recursive:
    
    datatools.workflow_utils
    datatools.datamodel_utils
    datatools.etl_utils
    datatools.run_doctests
    datatools.display_dataset
    datatools.stylesheet
    datatools._examples
    datatools._media_scrape
    datatools.models.media_pulse
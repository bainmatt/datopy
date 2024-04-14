"""
Runs doctests for all specified modules as a unittest suite.

Note
---- 
With `pytest` installed and configured to locate module imports correctly,
can also run `pytest --doctest-modules {optional_subpkg/module_name}`.
"""

from typing import Tuple
import doctest
import unittest
import pandas as pd


# TODO default to all modules and submodules

def run_doctest_suite(modules_to_test: Tuple[str, ...]):
    total_failures = 0
    results_by_module = {}
    n_modules = len(modules_to_test)
    
    for ix, module in enumerate(modules_to_test, start=1):
        start_message = f"Testing module {ix} / {n_modules}"
        print(f"\n\n{start_message} : {module}\n{'=' * len(start_message)}")
            
        # Run doctests by module and store results
        temp_module = __import__(module, fromlist=["*"])
        test_suite = doctest.DocTestSuite(temp_module)
        results = unittest.TextTestRunner().run(test_suite)
            
        # Store number and name of failed doctests
        failures = results.failures
        results_by_module[module] = {
            "n_failures": len(failures),
            "failed": [str(failure[0]).split(' (')[0] 
                       for failure in failures]   
        }        
        total_failures += len(failures)
        
    # Pretty print the results
    result_message = f"{total_failures} failures across {ix} module(s):"
    result_table = pd.DataFrame.from_dict(data=results_by_module,
                                          orient='index')
    print(f"\n\n{result_message}\n{'=' * len(result_message)}")
    print(result_table, '\n')    


if __name__ == "__main__":
    MODULES_TO_TEST = (
        'display_dataset', 
        'workflow_utils', 
        'datamodel_utils',
        'etl_utils',
        'models.media_pulse',
        '_media_scrape',  
        '_examples', 
    )
    
    run_doctest_suite(MODULES_TO_TEST)
from typing import Any
import doctest

### Save figs

### Save drive

### Other

def doctest_function(object: callable, globs: dict[str, Any]) -> None:
    """Convenience wrapper to run doctests for a specific function or class.

    Parameters
    ----------
    object : callable
        Class, function, or other object with doctests to be run.
    globs : dict[str, Any]
        Global variables from module of interest.
    """
    print('-------------------------------------------------------')
    finder = doctest.DocTestFinder(verbose=1, recurse=False)
    runner = doctest.DocTestRunner(verbose=1)
    for test in finder.find(obj=object, globs=globs):
        results = runner.run(test)
    print('-------------------------------------------------------')
    print(results)
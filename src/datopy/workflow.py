"""
Tools for data input/output.

Included:

- Saving figures and Jupyter runtime environment files
- Manually downloading modules
"""

import os
import doctest
import requests
import importlib
import urllib.request
from typing import Dict, List, Any, Callable


# TODO Save figs
### Save figs

# TODO Save drive
### Save drive

def git_module_loader(modules: Dict[str, List[str]],
                      save_dir: str | None = None,
                      run_tests: bool = False,
                      run_download: bool = False) -> None:
    """
    Securely downloads collections of modules directly from their Git repo.

    Retrieved files are stored in the current directory.

    Parameters
    ----------
    modules : Dict[str, List[str]]
        Keys are relative branch paths '{git-user}/{repo-name}/{branch-name}'.
        Values are lists of module filenames relative to their parent branch.

    run_tests : bool, default=False
        Whether or not to run doctests for successful downloads.

    run_download : bool, default=False
        Additional safeguard to ensure no modules are accidentally downloaded.

    Examples
    --------
    >>> from datopy.workflow import git_module_loader

    >>> modules = {'gitusername/repo/branch': ['module1.py', 'module2.py']}
    >>> git_module_loader(modules, run_tests=True, run_download=True)
    Module gitusername/repo/branch/module1.py does not exist.
    Module gitusername/repo/branch/module2.py does not exist.

    >>> modules = {"HIPS/autograd/master":
    ...     ['autograd/tracer.py', 'autograd/util.py']}
    >>> git_module_loader(modules, run_tests=False, run_download=False)
    Skipping download.
    Skipping download.
    """

    if not save_dir:
        save_dir = f"{os.path.dirname(os.path.abspath(__file__))}"
    else:
        pass

    for repo in modules:
        for module in modules[repo]:
            module_url = f"https://raw.githubusercontent.com/{repo}/{module}"
            exists = requests.head(
                module_url, allow_redirects=False).status_code == 200

            if not exists:
                print(f"Module {repo}/{module} does not exist.")
                continue

            filename = os.path.join(save_dir, os.path.basename(module))
            if os.path.isfile(filename):
                print(f"Module {repo}/{module} already downloaded.")
                continue

            if not run_download:
                print("Skipping download.")
                continue

            print(f"Downloading {repo}/{module}.")
            os.makedirs(save_dir, exist_ok=True)
            urllib.request.urlretrieve(url=module_url, filename=filename)

            if run_tests:
                print('Running tests:\n')
                module_name = module.split('/')[-1].split('.')[0]
                mod = importlib.import_module(module_name)
                doctest.testmod(mod, verbose=True)


### Efficient testing

def doctest_function(object: Callable[..., Any], globs: dict[str, Any],
                     verbose=True) -> None:
    """
    Run doctests for a specific function or class.

    Parameters
    ----------
    object : Callable[..., Any]
        Class, function, or other object with doctests to be run.
    globs : dict[str, Any]
        Global variables from module of interest.

    See Also
    --------
    datopy.run_doctests.run_doctest_suite :
        Simultaneously run all doctests across modules.
    """
    print('-------------------------------------------------------')
    finder = doctest.DocTestFinder(verbose=verbose, recurse=False)
    runner = doctest.DocTestRunner(verbose=verbose)
    for test in finder.find(obj=object, globs=globs):
        results = runner.run(test)
    print('-------------------------------------------------------')
    print(results)


def main():
    import doctest

    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod(verbose=True)
    # doctest_function(git_module_loader, globs=globals())


if __name__ == "__main__":
    main()

import os
import doctest
# import subprocess
import importlib
import requests
import urllib.request
from typing import Dict, List
from typing import Any

### Save figs

### Save drive

### Download Github modules

def git_module_loader(modules: Dict[str, List[str]], 
                      save_dir: str = f"{os.path.dirname(os.path.abspath(__file__))}",
                      run_tests: bool = False, 
                      run_download: bool = False) -> None:
    """Securely download collections of modules directly from their Git repo and store in current directory.

    Parameters
    ----------
    modules : Dict[str, List[str]]
        Keys are relative branch paths '{git-user}/{repo-name}/{branch-name}'.
        Values are lists of module filenames relative to their parent branch.
    run_tests : bool, default = False
        Whether or not to run doctests for successful downloads.
    run_download : bool, default = False
        Additional safeguard to ensure no modules are accidentally downloaded.

    Examples
    --------
    Negative example 1:
    >>> modules = {'gitusername/repo/branch': ['module1.py', 'module2.py']}
    >>> git_module_loader(modules, run_tests=1, run_download=1)
    Module gitusername/repo/branch/module1.py does not exist.
    Module gitusername/repo/branch/module2.py does not exist.
        
    Negative example 2:
    >>> modules = {
    ...     "HIPS/autograd/master":
    ...         ['autograd/tracer.py', 'autograd/util.py']
    ... }
    >>> git_module_loader(modules, run_tests=0, run_download=0)
    Skipping download.
    Skipping download.
    
    """

    for repo in modules:
        for module in modules[repo]:
            module_url = f"https://raw.githubusercontent.com/{repo}/{module}"
            exists = requests.head(
                module_url, allow_redirects=0).status_code == 200
            
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
            
            print(f"Downloading {repo}/{module}")
            os.makedirs(save_dir, exist_ok=1)
            urllib.request.urlretrieve(url=module_url, 
                                        filename=filename)
            
            if run_tests:
                print('Running tests:\n')
                module_name = module.split('.')[0]
                mod = importlib.import_module(module_name)
                doctest.testmod(mod, verbose=True)
                
                # TODO remove this fix
                # Magic command for Jupyter notebook use only
                # %run -i {module}

### Efficient testing

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

def main():
    import doctest
    
    # Comment out (2) to run all tests in script; (1) to run specific tests
    doctest.testmod(verbose=True)
    # doctest_function(git_module_loader, globs=globals())

if __name__ == "__main__":
    main()
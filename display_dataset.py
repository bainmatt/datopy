"""    
Tools for visualizing matrix and dataframe operations.

Notes
-----
- Adapted from [1] to support NumPy arrays, in addition to Pandas data frames.

References
----------
... [1] VanderPlas, J. (2016). Python data science handbook: Essential tools
        for working with data. "O'Reilly Media, Inc.".
"""

import numpy as np
import pandas as pd
from typing import Iterable, Any
import doctest
from nb_utils import doctest_function

class display(object):  
    """
    Display informative HTML representation of multiple objects side-by-side.
    
    Parameters
    ----------
    object : str
        String containing array-like or dataframe variable.
    *args : list, default=None
        Additional objects to display alongside the supplied `object`.

    Returns
    -------
    result
        Printout of formal object string representation.
        
    Examples
    --------
    Data frame example:
    >>> df1 = make_df('AB', [1, 2]); df2 = make_df('AB', [3, 4])
    >>> display('df1', 'df2', 'pd.concat([df1, df2])').r(globals(), bold=False)
    <BLANKLINE>
    df1
    --- (2, 2) ---
        A   B
    1  A1  B1
    2  A2  B2
    <BLANKLINE>
    <BLANKLINE>
    df2
    --- (2, 2) ---
        A   B
    3  A3  B3
    4  A4  B4
    <BLANKLINE>
    <BLANKLINE>
    pd.concat([df1, df2])
    --- (4, 2) ---
        A   B
    1  A1  B1
    2  A2  B2
    3  A3  B3
    4  A4  B4
    <BLANKLINE>
    <BLANKLINE>
    
    Matrix example:
    >>> A = np.array([[1, 3], [2, 4]]); x = np.array([[0, 1]])
    >>> display("A", "x.T", "np.dot(A, x.T)").r(globals(), bold=False)
    <BLANKLINE>
    A
    --- (2, 2) ---
    array([[1, 3],
           [2, 4]])
    <BLANKLINE>
    <BLANKLINE>
    x.T
    --- (2, 1) ---
    array([[0],
           [1]])
    <BLANKLINE>
    <BLANKLINE>
    np.dot(A, x.T)
    --- (2, 1) ---
    array([[3],
           [4]])
    <BLANKLINE>
    <BLANKLINE>
    
    """
    
    def __init__(self, *args, globs: dict[str, Any] = None, bold: bool = True):
        self.args = args
    
    # TODO ? move `globs` arg to constructor as class instance and 
    # ? use __repr__ to execute upon construction
    def r(self, globs: dict[str, Any] = None, bold: bool = True):    
        """
        Shorthand for `__repr__()`.

        Parameters
        ----------
        globs : dict[str, Any], default=None
            Global namespace, for access to eval() for nonlocals passed by name.
        bold : bool, default=True
            Option to disable string styling for testing purposes.
        """
        output = ""
        for arg in self.args:
            name = '\033[1m' + arg + '\033[0m' if bold else arg
            value = eval(arg, globs)
            shape = np.shape(value)
            rounded_value = np.round(value, 2)
            output += f"\n{name}\n--- {repr(shape)} ---\n{repr(rounded_value)}\n\n"

        print(output)
        return None


def make_df(cols: Iterable[Any], ind: Iterable[Any]) -> pd.DataFrame:
    """
    Quickly make a DataFrame.

    Parameters
    ----------
    cols : Iterable[Any]
        Iterable with items representing column names.
    ind : Iterable[Any]
        Iterable with items representing row names.

    Returns
    -------
    result : DataFrame of shape ( len(ind), len(cols) )
        
    Examples
    --------
    >>> import pandas as pd
    >>> make_df("ABC", [1,2,3])
        A   B   C
    1  A1  B1  C1
    2  A2  B2  C2
    3  A3  B3  C3
    
    >>> make_df([1,2,3], ("A", "B", "C"))
        1   2   3
    A  1A  2A  3A
    B  1B  2B  3B
    C  1C  2C  3C
    """

    data = {c: [str(c) + str(i) for i in ind] for c in cols}
    return pd.DataFrame(data, ind)    


def main():
    # Comment out (2) to run all tests in script; (1) to run specific tests
    # doctest.testmod(verbose=True)
    doctest_function(display, globs=globals())
    return None

if __name__ == "__main__":
    main()
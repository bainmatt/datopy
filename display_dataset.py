"""
Adapted from: 
    VanderPlas, J. (2016). Python data science handbook: Essential tools for working with data. "O'Reilly Media, Inc.".
Mofied to support NumPy arrays, in addition to Pandas data frames.
"""

import numpy as np
import pandas as pd
from typing import Iterable, Any

class display(object):  
    """Display HTML representation of multiple objects."""
    template = """<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}{1}
    
    Parameters
    ----------
        object : string containing array-like or dataframe variable
        *args : list, default=None
            Additional objects to display alongside `object`.

    Returns
    -------
        result :
            HTML respresentation.
        
    Examples
    --------
    # Execute module in Google Colab
    >>> run -i {'display_dataset.py'}
    
    >>> df = make_df("ABC", [1,2,3])
    >>> display('df')
    df
    --- (3, 3) ---
        A   B   C
    1  A1  B1  C1
    2  A2  B2  C2
    3  A3  B3  C3
    
    >>> df1 = make_df('AB', [1, 2])
    >>> df2 = make_df('AB', [3, 4])
    >>> display('df1', 'df2', 'pd.concat([df1, df2])')
    df1
    --- (2, 2) ---
        A   B
    1  A1  B1
    2  A2  B2


    df2
    --- (2, 2) ---
        A   B
    3  A3  B3
    4  A4  B4


    pd.concat([df1, df2])
    --- (4, 2) ---
        A   B
    1  A1  B1
    2  A2  B2
    3  A3  B3
    4  A4  B4
    """
    
    def __init__(self, *args):
        self.args = args
    
    def __repr__(self):
        return '\n\n'.join('\n' + '\033[1m' + a + '\033[0m'
            + '\n' + '--- ' + repr(np.shape(eval(a))) + ' ---'
            + '\n' + repr(np.round(eval(a), 2))
            for a in self.args
        )

def make_df(cols: Iterable[Any], ind: Iterable[Any]):
    """Quickly make a DataFrame.

    Parameters
    ----------
        cols : Iterable[Any]
            Iterable where items are column names.
        ind : Iterable[Any]
            Iterable where items are row names.

    Returns
    -------
        result : DataFrame
        
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
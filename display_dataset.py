"""
Adapted from: 
 VanderPlas, J. (2016). Python data science handbook: Essential tools for working with data. " O'Reilly Media, Inc.".
Mofied to support NumPy arrays, in addition to Pandas data frames.
"""

import numpy as np
import numpy.linalg as la
import pandas as pd

class display(object):
  """Display HTML representation of multiple objects"""
  template = """<div style="float: left; padding: 10px;">
  <p style='font-family:"Courier New", Courier, monospace'>{0}{1}
  """
  def __init__(self, *args):
    self.args = args

  def __repr__(self):
    return '\n\n'.join(
        '\n' + '\033[1m' + a + '\033[0m'
        + '\n' + '--- ' + repr(np.shape(eval(a))) + ' ---'
        + '\n' + repr(np.round(eval(a), 2))
        for a in self.args
    )

def make_df(cols, ind):
  """Quickly make a DataFrame"""
  data = {c: [str(c) + str(i) for i in ind]
          for c in cols}
  return pd.DataFrame(data, ind)
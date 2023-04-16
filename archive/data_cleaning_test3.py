import pandas as pd
import pytest
import sys

packages_path = '/Users/samlafell/Desktop/over_under_project/utils'
if packages_path not in sys.path:
    sys.path.append(packages_path)

from data_cleaning import remove_invalid_vals

df1 = pd.DataFrame({'col1': [1, 2, False, -1], 'col2': [4, 5, 6, -1], 'col3': [0, 8, 9, 'bird']})
invalid_vals = [-1, 0, 'bird', False]
col_search = ['col1', 'col2', 'col3']
df2 = pd.DataFrame({'col1': [2], 'col2': [5], 'col3': [8]}, dtype=object)

remove_invalid_vals(df1, invalid_vals, col_search)
df2

pd.testing.assert_frame_equal(remove_invalid_vals(df1, invalid_vals, col_search), df2)






remove_invalid_vals(df1, invalid_vals, col_search)
pd.testing.assert_frame_equal(remove_invalid_vals(df1, invalid_vals, col_search), df2)
import pytest
import pandas as pd
from utils import data_cleaning as dc


expected_output = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]})
@pytest.mark.parametrize('data', pd.DataFrame({'col1': [1, 2, 3, -1], 'col2': [4, 5, 6, -1], 'col3': [7, 8, 9, -1]}))
@pytest.mark.parametrize('invalid_vals', [-1])
@pytest.mark.parametrize('cols', ['col1, col3'])
def test_remove_invalid_vals(data, invalid_vals, cols):
    assert dc.remove_invalid_vals(data, invalid_vals, cols).equals(expected_output), f'Expected {expected_output}, got {dc.remove_invalid_vals(data, invalid_vals, cols)}'
    

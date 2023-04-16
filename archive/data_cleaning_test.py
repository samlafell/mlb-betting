import pandas as pd
from utils import data_cleaning as dc

def test_remove_invalid_vals(invalid_vals=None, cols=None):
    
    # First Test
    if invalid_vals is None:
        invalid_vals = [-1]
    if cols is None:
        cols = ['col1', 'col2', 'col3']
    
    test_data = {'col1': [1, 2, 3, -1], 'col2': [4, 5, 6, -1], 'col3': [7, 8, 9, -1]}
    df = pd.DataFrame(test_data)

    # Call the function and check the output
    result = dc.remove_invalid_vals(df, invalid_vals, cols)
    expected_output = {'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]}
    expected_output = pd.DataFrame(expected_output)
    pd.testing.assert_frame_equal(result, expected_output), f'Expected {expected_output}, got {result}'
    
    
    # Second Test
    invalid_vals = [-1, 0, 'bird', False]
    cols = ['col1', 'col2', 'col3']
        
    test_data = {'col1': [1, 2, False, -1], 'col2': [4, 5, 6, -1], 'col3': [0, 8, 9, 'bird']}
    df = pd.DataFrame(test_data)
    
    # Call the function and check the output
    result = dc.remove_invalid_vals(df, invalid_vals, cols).apply(lambda x: x.astype(object))
    expected_output = {'col1': [2], 'col2': [5], 'col3': [8]}
    expected_output = pd.DataFrame(expected_output).apply(lambda x: x.astype(object))
    assert result.equals(expected_output), f'Expected {expected_output}, got {result}'
    
test_remove_invalid_vals()
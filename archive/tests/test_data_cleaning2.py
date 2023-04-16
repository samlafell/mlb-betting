import pytest
import pandas as pd
import data_cleaning as dc

@pytest.fixture
def example_data():
    return {
            "input": pd.DataFrame({'col1': [1, 2, 3, -1], 'col2': [4, 5, 6, -1], 'col3': [7, 8, 9, -1]}),
            "invalid_cols": [-1],
            "cols":['col1', 'col3']
            }

example_data

assert dc.remove_invalid_vals(example_data) == pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]})



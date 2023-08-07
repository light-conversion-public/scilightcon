import numpy as np
from importlib import resources
import pickle
import scilightcon
from scilightcon.utils._fixes import _open_binary
from scilightcon.fitting import fit_beam_profile_2d
import pytest

def test_fitting_beam_profiler():
    with _open_binary(scilightcon.datasets.DATA_MODULE, 'test_beam_profile.pkl') as filepath:
        matrix = pickle.load(filepath)['matrix']
        
    output = fit_beam_profile_2d (matrix, method = 'gauss', options = {'decimation' : 2})

    # 1 - raises ValueError when method not found
    with pytest.raises(ValueError):
        fit_beam_profile_2d(matrix, method='idk', options = {})

    # 2 - checks if mean_x value is within the specified range
    mean_x = output.get('mean_x')
    assert 93.0 <= mean_x <= 95.0, "mean_x is not within the specified range"

    # 3 - checks if mean_y value is within the specified range
    mean_y = output.get('mean_y')
    assert 65.0 <= mean_y <= 67.0, "mean_y is not within the specified range"

    # 4 - checks if sigma_x value is within the specified range
    sigma_x = output.get('sigma_x')
    assert 30.0 <= sigma_x <= 33.0, "sigma_x is not within the specified range"   

    # 5 - checks if sigma_y value is within the specified range
    sigma_y = output.get('sigma_y')
    assert 29.0 <= sigma_y <= 33.0, "sigma_y is not within the specified range"      

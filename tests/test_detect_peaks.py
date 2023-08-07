import scilightcon
import pytest
from scilightcon.fitting import detect_peaks    
from scilightcon.datasets import load_csv_data
import numpy as np

def test_detect_peaks():
    data, headers = load_csv_data('data_test_detect_peaks.csv')
    x = data[:,0]
    y = data[:,1]

    peaks = detect_peaks(x, y, method='above_average', n_max=2, options = {})
    assert (peaks == [[22, 25], [12, 15]])

    # 1 - raises ValueError when method not found
    with pytest.raises(ValueError):
        detect_peaks(x, y, method='idk', n_max=2, options = {})
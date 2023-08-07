import pytest
import numpy as np
import scilightcon
from scilightcon.datasets import load_zipped_csv_data

def test_load_EKSMA_OPTICS_mirror_reflections():
    from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections

    data, headers = load_EKSMA_OPTICS_mirror_reflections('Ag')
    assert (np.shape(data) == (172,2))

    data, headers = load_EKSMA_OPTICS_mirror_reflections('Al')
    assert (np.shape(data) == (168,2))

    data, headers = load_EKSMA_OPTICS_mirror_reflections('Au')
    assert (np.shape(data) == (182,2))

    with pytest.raises(ValueError):
        _,_ = load_EKSMA_OPTICS_mirror_reflections('Other')
    
def test_load_csv_data():
    from scilightcon.datasets import load_csv_data

    data, headers = load_csv_data('Hg_lines.csv')
    assert (np.shape(data) == (25,2))

    data, headers = load_csv_data('Ar_lines.csv')
    assert (np.shape(data) == (122,2))
    data, headers = load_csv_data('White_LED_spectrum.csv')
    assert (np.shape(data) == (239,2))

    with pytest.raises(ValueError):
        try:
            _,_ = load_csv_data('Other')
        except FileNotFoundError:
            raise ValueError
        
def test_load_zipped_csv_data():

    actual_data, actual_header = scilightcon.datasets.load_zipped_csv_data('data_test_detect_peaks.csv.gz')
    target_data, target_header = scilightcon.datasets.load_csv_data('data_test_detect_peaks.csv')
    
    assert (actual_header == target_header) 
    print((actual_data))
    print((target_data))
    assert (np.all(np.array(actual_data) == np.array(target_data)))

    with pytest.raises(ValueError):
        try:
            _,_ = load_zipped_csv_data('Other')
        except FileNotFoundError:
            raise ValueError

def load_EO_filter_transmissions():
    from scilightcon.datasets import load_EO_filter_transmissions

    data, headers = load_EO_filter_transmissions('lp_400nm')
    assert (np.shape(data) == (1209,2))

    data, headers = load_EO_filter_transmissions('lp_450nm')
    assert (np.shape(data) == (1297,2))

    data, headers = load_EO_filter_transmissions('lp_500nm')
    assert (np.shape(data) == (1315,2))

    with pytest.raises(ValueError):
        _,_ = load_EO_filter_transmissions('Other')

def load_EO_filter_transmissions():
    from scilightcon.datasets import load_EO_filter_transmissions

    data, headers = load_EO_filter_transmissions('DMLP425')
    assert (np.shape(data) == (2251,2))

    data, headers = load_EO_filter_transmissions('DMLP550')
    assert (np.shape(data) == (2251,2))

    data, headers = load_EO_filter_transmissions('DMLP650')
    assert (np.shape(data) == (2251,2))

    with pytest.raises(ValueError):
        _,_ = load_EO_filter_transmissions('Other')

def load_atmospheric_data():
    from scilightcon.datasets import load_atmospheric_data

    data, headers = load_atmospheric_data('atmosphere.csv')
    assert (np.shape(data) == (20407,2))

    with pytest.raises(ValueError):
        try:
            _,_ = load_atmospheric_data('Other')
        except FileNotFoundError:
            raise ValueError

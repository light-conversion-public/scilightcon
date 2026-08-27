import pytest
import numpy as np
import scilightcon
from scilightcon.datasets import load_zipped_csv_data

def assert_spectrum_shape(data):
    assert (np.shape(data)[1] == 2)
    assert (np.shape(data)[0] > 10)

def test_load_spectrum():
    from scilightcon.datasets import load_spectrum
    data, header = load_spectrum('thorlabs', 'DMLP425', 't')
    assert_spectrum_shape(data)

    with pytest.raises(ValueError):
        load_spectrum('undefined_vendor', 'x')

    with pytest.raises(ValueError):
        load_spectrum('thorlabs', 'undefined_filter')

    with pytest.raises(ValueError):
        load_spectrum('thorlabs', 'DMLP425', 'undefined_mode')

def test_load_thorlabs_spectrum():
    from scilightcon.datasets import load_THORLABS_filter_transmissions
    data, header = load_THORLABS_filter_transmissions('DMLP425', 't')
    assert_spectrum_shape(data)

    with pytest.raises(ValueError):
    _,_ = load_THORLABS_filter_transmissions('Other')

def test_load_chroma_spectrum():
    from scilightcon.datasets import load_chroma_spectrum

    data, headers = load_chroma_spectrum('ET340X')
    assert_spectrum_shape(data)

    with pytest.raises(ValueError):
        _,_ = load_chroma_spectrum('Other')

def test_load_eksma_spectrum():
    from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections

    data, headers = load_EKSMA_OPTICS_mirror_reflections('Ag')
    assert_spectrum_shape(data)

    with pytest.raises(ValueError):
        _,_ = load_EKSMA_OPTICS_mirror_reflections('Other')

def test_load_hamamatsu_spectrum():
    from scilightcon.datasets import load_hamamatsu_qe

    data, headers = load_hamamatsu_qe('H10721-210')
    assert_spectrum_shape(data)

    with pytest.raises(ValueError):
        _,_ = load_hamamatsu_qe('Other')

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

def load_atmospheric_data():
    from scilightcon.datasets import load_atmospheric_data

    data, headers = load_atmospheric_data('atmosphere.csv')
    assert (np.shape(data) == (20407,2))

    with pytest.raises(ValueError):
        try:
            _,_ = load_atmospheric_data('Other')
        except FileNotFoundError:
            raise ValueError

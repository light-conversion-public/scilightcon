import pytest
import numpy as np

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



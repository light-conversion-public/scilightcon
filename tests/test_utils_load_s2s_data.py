import scilightcon
from scilightcon.utils import load_s2s_data
from scilightcon.utils._fixes import _get_path

def test_utils_load_s2s_data():
    s2s_data = load_s2s_data(str(_get_path(scilightcon.datasets.DATA_MODULE, 'Shot-to-shot_LAB4 PHAROS_25.0kHz_1030nm_InGaAs_20210917_1337.s2s')))
    assert(len(s2s_data.outliers) == 5)

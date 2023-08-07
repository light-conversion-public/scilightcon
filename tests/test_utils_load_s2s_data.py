import scilightcon
from scilightcon.utils import load_s2s_data
from scilightcon.utils._fixes import _get_path
from importlib import resources

def test_utils_load_s2s_data():

    with _get_path(scilightcon.datasets.DATA_MODULE, 'Shot-to-shot_LAB4 PHAROS_25.0kHz_1030nm_InGaAs_20210917_1337.s2s') as filepath:
        s2s_data = load_s2s_data(filepath)

    assert(len(s2s_data.outliers) == 5)
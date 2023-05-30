import scilightcon
from scilightcon.utils import load_s2s_data
from importlib import resources

def test_utils_load_s2s_data():

    filepath = resources.files(scilightcon.datasets.DATA_MODULE).joinpath('Shot-to-shot_LAB4 PHAROS_25.0kHz_1030nm_InGaAs_20210917_1337.s2s')

    s2s_data = load_s2s_data(filepath)

    assert(len(s2s_data).outliers == 4)
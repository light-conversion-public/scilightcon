from typing import List
import numpy as np
from typing import List, Tuple
from scipy.interpolate import interp1d


def _get_refractive_index_from_raw_data(x0: float, x: List[float], y: List[float]) -> float:
    '''This function interpolates x,y data and returns function's value at x0'''
    f2 = interp1d(x, y, kind = "linear") 
    return f2(x0)
from scipy.interpolate import interp1d
import numpy as np
from typing import Tuple, List

def interpolate_and_multiply(
        D1: Tuple[List[float], List[float]], 
        D2: Tuple[List[float], List[float]]) -> Tuple[List[float], List[float]] :
    """Takes D2 array and interpolates x an y in respect to array from D1. Then takes an array form D2 and adujst its range according to D1
    and multiply two arrays.


    Args:
        D1 (tuple): An array  to which respect we interpolate anoter array.
        D2 (tuple): An array which x and y values are interpolated.

    Returns:
        A matrix which is a product of `D1` and interpolated `D2`.
    """

    #interpolates D2 values according to D1 and selecting the range
    x2 = D2[:,0]
    y2 = D2[:,1]
    interpolated_function = interp1d(x2, y2, bounds_error = False, fill_value = None)

    x1 = D1[:,0]
    y1 = D1[:,1]
    y2_interpolated = interpolated_function(x1)

    y3 = y1 * y2_interpolated

    D4 = np.transpose([x1, y3])

    #removing all rows with nan values
    D5 = (D4[~np.isnan(D4).any(axis=1)])

    #Multiply D1 and D6
    return D5

from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections
from scipy.interpolate import interp1d
import numpy as np

def interpolate_and_multiply(D1, D2):

    #interpolates D2 valus according to D1 and selecting the range
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

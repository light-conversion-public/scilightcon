import pandas as pd
import numpy as np
from pathlib import Path

def thorlabs_xls_to_csv(file_name, mode='trans'):
    """
    XLS to CSV converter for Thorlabs filter and mirror transmission and
    reflection data.

    Examples:

        >>> from scilightcon.datasets import thorlabs_xls_to_csv # doctest: +SKIP
        >>> wavl, trans = thorlabs_xls_to_csv('DMLP505.xls') # doctest: +SKIP
    """
    data = pd.read_excel(file_name, usecols='C:E')

    wavl = np.array(data.iloc[:, 0], dtype='int')

    if mode == 'trans':
        ydata = np.array(data.iloc[:, 1])
        preffix = 'transmission'
        yunits = 'Transmission (%)'
        if not 'transmi' in data.columns[1].lower():
            raise ValueError("Second column is not transmission")
    elif mode == 'refl':
        ydata = np.array(data.iloc[:, 2])
        preffix = 'reflection'
        yunits = 'Reflectance (%)'
        if not 'reflec' in data.columns[2].lower():
            raise ValueError("Second column is not reflectance")

    if not 'wavelength' in data.columns[0].lower():
        raise ValueError("First column is not wavelength")

    if not 'nm' in data.columns[0].lower():
        raise ValueError("Wavelength is not in nm")

    if not '%' in data.columns[1].lower():
        raise ValueError("Data is not in %")

    if np.min(wavl < 0):
        raise ValueError("Wavelength < 0")

    if np.max(wavl < 100):
        raise ValueError("Wavelength is probably not in nm")

    if np.min(ydata) < -1:
        raise ValueError("Y data (transmission or reflectance) < 0%")

    if np.max(ydata) < 2:
        raise ValueError("Y data (transmission or reflectance) is probably not in %")


    np.savetxt(f"{preffix}_THORLABS_{Path(file_name).stem}.csv",
            np.transpose([wavl, ydata]),
            header=f"Wavelength  (nm), {yunits}",
            fmt="%.6f",
            delimiter=', ')

    return wavl, ydata

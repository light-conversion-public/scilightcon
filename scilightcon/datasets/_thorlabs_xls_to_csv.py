import pandas as pd
import numpy as np
from pathlib import Path

def thorlabs_xls_to_csv(file_name):
    """
    XLS to CSV converter for Thorlabs filter and mirror transmission and
    reflection data.

    Examples:

        >>> from scilightcon.datasets import thorlabs_xls_to_csv # doctest: +SKIP
        >>> wavl, trans = thorlabs_xls_to_csv('DMLP505.xls') # doctest: +SKIP
    """
    data = pd.read_excel(file_name, skiprows=1, usecols='C:E')

    wavl = np.array(data.iloc[:, 0], dtype='int')
    trans = np.array(data.iloc[:, 1])

    if not 'wavelength' in data.columns[0].lower():
        raise ValueError("First column is not wavelength")

    if not 'nm' in data.columns[0].lower():
        raise ValueError("Wavelength is not in nm")

    if not 'transmi' in data.columns[1].lower():
        raise ValueError("Second column is not transmission")

    if not '%' in data.columns[1].lower():
        raise ValueError("Transmission is not in %")

    if np.min(wavl < 0):
        raise ValueError("Wavelength < 0")

    if np.max(wavl < 100):
        raise ValueError("Wavelength is probably not in nm")

    if np.min(trans) < 0:
        raise ValueError("Transmission < 0")

    if np.max(trans) < 2:
        raise ValueError("Transmission is probably not in %")

    np.savetxt(f"transmission_THORLABS_{Path(file_name).stem}.csv",
            np.transpose([wavl, trans]),
            header="Wavelength  (nm), Transmission (%)",
            fmt="%.6f",
            delimiter=', ')

    return wavl, trans



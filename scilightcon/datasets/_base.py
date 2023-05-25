"""
Base data loading code for all datasets
"""

import csv
import gzip
import os
from ..utils.fixes import _open_text, _open_binary
from typing import Tuple, List
from typing_extensions import Literal
import pickle

import numpy as np

DATA_MODULE = "scilightcon.datasets.data"
MATERIALS_PICKLE_FILENAME = "toolbox_materials.pkl"

def load_csv_data(
    data_file_name,
    *,
    data_module=DATA_MODULE
):
    """Loads `data_file_name` from `data_module with `importlib.resources`.
    Parameters
    ----------
    data_file_name : str
        Name of csv file to be loaded from `data_module/data_file_name`.
        For example `'wine_data.csv'`.
    data_module : str or module, default='scilightcon.datasets.data'
        Module where data lives. The default is `'scilightcon.datasets.data'`.
    Returns
    -------
    data : ndarray of shape (n_samples, n_features)
        A 2D array with each row representing one sample and each column
        representing the features of a given sample.
    target : ndarry of shape (n_samples,)
        A 1D array holding target variables for all the samples in `data`.
        For example target[0] is the target variable for data[0].
    target_names : ndarry of shape (n_samples,)
        A 1D array containing the names of the classifications. For example
        target_names[0] is the name of the target[0] class.
    """
    with _open_text(data_module, data_file_name) as csv_file:
        data_file = csv.reader(csv_file)
        n_header = 0
        possibly_header = next(data_file)
        header = [''] * len(possibly_header)
        is_header = possibly_header[0][0] == '#'
        if is_header:            
            header = possibly_header
            header[0] = header[0][1:]
            header = [entry.strip() for entry in header]

        while is_header:
            n_header = n_header + 1
            is_header = next(data_file)[0][0] == '#'

        csv_file.seek(n_header)
        n_samples = sum(1 for row in data_file) - n_header
        csv_file.seek(n_header)
        temp = next(data_file)
        n_features = len(temp)
        csv_file.seek(n_header)
        data = np.empty((n_samples, n_features))

        for i, ir in enumerate(data_file):
            if i>=n_header:
                data[i-n_header] = np.asarray(ir, dtype=np.float64)

    return data, header

def load_EKSMA_OPTICS_mirror_reflections(
    material: Literal['Al', 'Ag', 'Au']
) -> Tuple[np.ndarray, list]:
    """Loads wavelength-dependent reflection dataset of metal coated mirrors
    by [EKSMA OPTICS](https://eksmaoptics.com/optical-components/metallic-mirrors/protected-aluminium-mirrors).

    Examples:
        >>> from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections
        >>> data, header = load_EKSMA_OPTICS_mirror_reflections('Ag')
        >>> np.shape(data)
        (172, 2)
        >>> header
        ['Wavelength (nm)', 'Reflection (%)']


    Args:
        material (str): `Ag`, `Au` or `Al`

    Returns:
        data : ndarray of shape (n_samples, n_columns)
            A 2D array of data with headers excluded.
        header : list of shape (n_columns) of column names or empty strings

    """
    data_file_name = 'reflection_EKSMA_{:}.csv'.format(material)

    try:
        data, header = load_csv_data(
            data_file_name=data_file_name
        )
    except FileNotFoundError:
        raise ValueError

    return data, header

def load_materials():
    """
    Loads material database as scilightcon.datasets.materials
    """    
    with _open_binary(DATA_MODULE, MATERIALS_PICKLE_FILENAME) as f:
        materials = pickle.load(f)
        return materials

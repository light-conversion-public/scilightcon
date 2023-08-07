"""Base data loading code for all datasets

"""
import csv
import gzip
import os
import pickle
import numpy as np
import shutil
import tempfile
from typing import Tuple, List
from typing_extensions import Literal
import scilightcon
from ..utils._fixes import _open_text, _open_binary
from scilightcon.utils._fixes import _get_path

DATA_MODULE = "scilightcon.datasets.data"
DATA_MODULE_THORLABS = "scilightcon.datasets.data.thorlabs"
DATA_MODULE_EO = "scilightcon.datasets.data.EO"
MATERIALS_PICKLE_FILENAME = "toolbox_materials.pkl"

def load_csv_data(
    data_file_name,
    *,
    data_module=DATA_MODULE
):
    """
    Loads `data_file_name` from `data_module` with `importlib.resources`.
    
    Examples:
        >>> from scilightcon.datasets import load_csv_data
        >>> data, header = load_csv_data('Hg_lines.csv')

    Args:
        data_file_name (str): Name of csv file to be loaded from `data_module/data_file_name`. 
        data_module (str or module):  Module where data lives. The default is `'scilightcon.datasets.data'`
   
    Returns:
        data (ndarray): A 2D array with each row representing one sample and each column representing the features of a given sample. Shape: n_samples, n_features
        target (ndarry): A 1D array holding target variables for all the samples in `data`. For example target[0] is the target variable for data[0]. Shape (n_samples,)
        target_names (ndarry): A 1D array containing the names of the classifications. For example target_names[0] is the name of the target[0] class. Shape (n_samples,)

    """
    with _get_path(data_module, data_file_name) as csv_file_path:
        return _read_csv_file(csv_file_path)

def _read_csv_file(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
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

def load_zipped_csv_data(data_file_name, *, data_module=DATA_MODULE):
    """Extracts gzip file to csv.
    
    Examples:
        >>> from scilightcon.datasets import load_zipped_csv_data # doctest: +SKIP
        >>> data_file_name = r'C:\Code\lightcon-scipack\scilightcon\datasets\data\data_test_detect_peaks.csv.gz' # doctest: +SKIP
        >>> data, header = _load_zipped_csv_data(data_file_name) # doctest: +SKIP
        
    Args:
        data_file_name (str): Path of the file that needs to be extracted
        data_module (str or module):  Module where data lives. The default is `'scilightcon.datasets.data'`

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)    
        header (List): Column names or empty strings. Shape (n_columns)
    """
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'extracted.csv') 

    with _get_path(scilightcon.datasets.DATA_MODULE, data_file_name) as gz_file_path:
        with gzip.open(gz_file_path, 'r') as file_in:
             with open(temp_path, 'wb') as file_out:
                shutil.copyfileobj(file_in, file_out)
    
    return _read_csv_file(temp_path)

def load_EO_filter_transmissions(
        filter: Literal
) -> Tuple[np.ndarray, list]:
    """Loads wavelength-dependent transmission dataset of chosen filter from EO file. Stock number is indicated in the second line of the dataset.

    Examples:
        >>> from scilightcon.datasets import load_EO_filter_transmissions
        >>> data, header = load_EO_filter_transmissions('lp_450nm')
        >>> np.shape(data)
        (1297, 2)
        >>> header
        ['Wavelength (nm)', 'Transmission (%)']

    Args:
        filter (str): `lp_400nm`, `lp_450nm`, `lp_500nm`, `lp_550nm`, `lp_600nm`, `lp_600nm`, `lp_700nm`, `lp_750nm`, `sp_400nm`, `sp_500nm`, `sp_600nm` or `sp_700nm`

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)  
        header (List): Column names or empty strings. Shape (n_columns)
    """
    data_file_name = 'transmission_EO_{:}.csv'.format(filter)

    try:
        data, header = load_csv_data(
            data_file_name=data_file_name,
            data_module=DATA_MODULE_EO
        )
    except FileNotFoundError:
        raise ValueError

    return data, header

def load_THORLABS_filter_transmissions(
        filter: Literal
) -> Tuple[np.ndarray, list]:
    """Loads wavelength-dependent transmission dataset of chosen material from thorlabs file.

    Examples:
        >>> from scilightcon.datasets import load_THORLABS_filter_transmissions
        >>> data, header = load_THORLABS_filter_transmissions('DMLP425')
        >>> np.shape(data)
        (2251, 2)
        >>> header
        ['Wavelength  (nm)', 'Transmission (%)']

    Args:
        filter (str): `DMLP425`, `DMLP550`, `DMLP650`, `FB340-10`, `FBH343-10`, `FBH400-40`, `FBH515-10`, `FBH520-40`, `FBH550-40`, `FEL0400`, `FEL0450`, `FEL0500`, `FEL0550`, `FEL0600`, `FEL0650`, `FEL0700`, `FEL0750`, `FEL0800`, `FEL0850`, `FEL0900`, `FEL0950`, `FEL1000`, `FEL1050`, `FEL1100`, `FEL1150`, `FEL1200`, `FEL1250`, `FEL01300`, `FEL1350`, `FEL1400`, `FEL1450`, `FEL1500`, `FELH1000`, `FELH1050`, `FELH1100`, `FELH1250`, `FELH1500`, `FES0450`, `FES0500`, `FES0550`, `FES0600`, `FES0650`, `FES0700`, `FES0750`, `FES0800`, `FES0850`, `FES0900`, `FES0950`, `FES1000`, `FESH0450`, `FES0500`, `FES0600`, `FES0700`, `FES0750`,  `FGB37`, `FGB39`, `FGS550`, `FGS700`, `FGS900`, `FGUV5`, `FGUV11`, `FL514.5-10`, `FL530-10`, `MF460-60`, `NDUV01B`, `NDUV02B`, `NDUV06B`, `NDUV10B`, `NDUV20B`, `NDUV30B`, `NDUV40B`, `NE01B`, `NE06B`, `NE10B`, `NE20B`, `NE30B`, `NE40B`, `NE50B` or `NE60B` 

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)
        header (List): Column names or empty strings. Shape (n_columns)
    """
    data_file_name = 'transmission_THORLABS_{:}.csv'.format(filter)

    try:
        data, header = load_csv_data(
            data_file_name=data_file_name,
            data_module=DATA_MODULE_THORLABS
        )
    except FileNotFoundError:
        raise ValueError

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
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns) 
        header (List): Column names or empty strings. Shape (n_columns)

    """
    data_file_name = 'reflection_EKSMA_{:}.csv'.format(material)

    try:
        data, header = load_csv_data(
            data_file_name=data_file_name
        )
    except FileNotFoundError:
        raise ValueError

    return data, header

def load_atmospheric_data() -> Tuple[np.ndarray, list]:
    """
    Loads atmospheric data.
    
    Examples:
        >>> from scilightcon.datasets import load_atmospheric_data
        >>> data, header = load_atmospheric_data()
    
    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)
        header (List): Column names or empty strings. Shape (n_columns)

    """
    data_file_name = 'atmosphere.csv'

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

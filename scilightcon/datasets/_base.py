"""Base data loading code for all datasets

"""
import csv
import gzip
import os
import pickle
import numpy as np
import shutil
import tempfile
from typing import Tuple
from typing_extensions import Literal

import scilightcon
from ..utils._fixes import _open_binary
from scilightcon.utils._fixes import _get_path

DATA_MODULE = "scilightcon.datasets.data"
DATA_MODULE_THORLABS = "scilightcon.datasets.data.thorlabs"
DATA_MODULE_CHROMA = "scilightcon.datasets.data.chroma"
DATA_MODULE_EO = "scilightcon.datasets.data.EO"
DATA_MODULE_HAMAMATSU = "scilightcon.datasets.data.Hamamatsu"
DATA_MODULE_EMITTERS = "scilightcon.datasets.data.Emitters"
DATA_MODULE_MISC = "scilightcon.datasets.data.misc"
MATERIALS_PICKLE_FILENAME = "toolbox_materials.pkl"

# Vendor-specific name Literals. Need to be updated manually when new dataset
# entries are added.
HamamatsuDetectorName = Literal[
    'H10721-01', 'H10721-110', 'H10721-210', 'H7422-40', 'H7422-50'
]

ThorlabsFilterName = Literal[
    'DMLP425', 'DMLP463', 'DMLP505', 'DMLP550', 'DMLP567', 'DMLP650', 'DMLP735B',
    'DMSP490', 'DMSP550', 'DMSP805', 'FB340-10', 'FBH343-10', 'FBH390-10',
    'FBH400-40', 'FBH515-10', 'FBH520-40', 'FBH550-40', 'FBH600-40', 'FEL0400',
    'FEL0450', 'FEL0500', 'FEL0550', 'FEL0600', 'FEL0650', 'FEL0700', 'FEL0750',
    'FEL0800', 'FEL0850', 'FEL0900', 'FEL0950', 'FEL1000', 'FEL1050', 'FEL1100',
    'FEL1150', 'FEL1200', 'FEL1250', 'FEL1300', 'FEL1350', 'FEL1400', 'FEL1450',
    'FEL1500', 'FELH0550', 'FELH1000', 'FELH1050', 'FELH1100', 'FELH1250',
    'FELH1500', 'FES0450', 'FES0500', 'FES0550', 'FES0600', 'FES0650', 'FES0700',
    'FES0750', 'FES0800', 'FES0850', 'FES0900', 'FES0950', 'FES1000', 'FESH0450',
    'FESH0500', 'FESH0600', 'FESH0700', 'FESH0750', 'FESH0900', 'FGB37', 'FGB39',
    'FGS550', 'FGS700', 'FGS900', 'FGUV11', 'FGUV5', 'FL514.5-10', 'FL530-10',
    'M254H45', 'MF434-17', 'MF460-60', 'MF525-39', 'NDUV01B', 'NDUV02B',
    'NDUV06B', 'NDUV10B', 'NDUV20B', 'NDUV30B', 'NDUV40B', 'NE01B', 'NE06B',
    'NE10B', 'NE20B', 'NE30B', 'NE40B', 'NE50B', 'NE60B',
]

EksmaMirrorMaterial = Literal['Ag', 'Al', 'Au']

ChromaFilterName = Literal['ET340X']

VendorName = Literal['thorlabs', 'eo', 'chroma', 'eksma', 'hamamatsu', 'emitters', 'misc']

# Vendor-based file formats
_VENDOR_FMTS = {
    'thorlabs': dict(module=DATA_MODULE_THORLABS, template='{suffix}_THORLABS_{name}.csv'),
    'eo': dict(module=DATA_MODULE_EO, template='{suffix}_EO_{name}.csv'),
    'chroma': dict(module=DATA_MODULE_CHROMA, template='{suffix}_CHROMA_{name}.csv'),
    'eksma': dict(module=DATA_MODULE, template='reflection_EKSMA_{name}.csv'),
    'hamamatsu': dict(module=DATA_MODULE_HAMAMATSU, template='qe_Hamamatsu_{name}.csv'),
    'emitters': dict(module=DATA_MODULE_EMITTERS, template='{name}_{suffix}.csv'),
    'misc': dict(module=DATA_MODULE_MISC, template='{name}_{suffix}.csv')
}


def load_spectrum(
        vendor: VendorName,
        name: str,
        mode: Literal['t', 'r', 'ex', 'em', '2pex'],
) -> Tuple[np.ndarray, list]:
    """Load a transmission, reflection or quantum efficiency spectrum
    for a named optic or detector from one of the vendor datasets bundled with
    scilightcon.

    This is the generic loader behind `load_hamamatsu_spectrum`,
    `load_thorlabs_spectrum`, `load_eksma_spectrum` and `load_chroma_spectrum`.
    Prefer those vendor-specific functions when the vendor is known ahead of
    time: their `name` argument typed via `Literal` to available filters and
    detectors.

    Examples:
        >>> from scilightcon.datasets import load_spectrum
        >>> data, header = load_spectrum('thorlabs', 'DMLP425', mode='t')
        >>> np.shape(data)
        (2251, 2)
        >>> header
        ['Wavelength  (nm)', 'Transmission (%)']

    Args:
        source (str): `hamamatsu`, `thorlabs`, `eksma` or `chroma`.
        name (str): Vendor-specific filter/detector/material name, e.g. `DMLP425` for `thorlabs`. See `load_hamamatsu_spectrum`, `load_thorlabs_spectrum`, `load_eksma_spectrum` and `load_chroma_spectrum` for the valid names per vendor.
        mode (str): `t` for transmission, `r` for reflection. Ignored by vendors that only publish one direction (`hamamatsu` QE curves, `eksma` mirror reflections).

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)
        header (List): Column names or empty strings. Shape (n_columns)
    """
    vendor = vendor.lower()
    mode = mode.lower()

    try:
        config = _VENDOR_FMTS[vendor.lower()]
    except KeyError:
        raise ValueError(
            f"Unknown spectrum source '{vendor}'. Valid sources: "
            f"{', '.join(_VENDOR_FMTS)}"
        )

    if vendor == 'hamamatsu' and mode == 'qe':
        suffix = 'qe'
    elif vendor == 'emitters' and mode in ['ex', 'em', '2pex']:
        suffix = mode
    elif mode == 't':
        suffix = 'transmission'
    elif mode == 'r':
        suffix = 'reflection'
    else:
        raise ValueError(f"Invalid mode '{mode}'")

    data_file_name = config['template'].format(name=name, suffix=suffix)

    try:
        data, header = load_csv_data(
            data_file_name=data_file_name,
            data_module=config['module']
        )
    except FileNotFoundError:
        raise ValueError

    # Return percent in [0, 1] range for multiplication
    data[:,1] = data[:,1]/100

    return data, header


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
    return _read_csv_file(_get_path(data_module, data_file_name))

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

        # Data format is expected in last header line
        csv_file.seek(0)
        for ind in range(n_header):
            last_col_header = next(data_file)
            
        n_samples = sum(1 for row in data_file)
        n_features = len(last_col_header)
        data = np.empty((n_samples, n_features))

        csv_file.seek(0)
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

    with gzip.open(str(_get_path(scilightcon.datasets.DATA_MODULE, data_file_name)), 'r') as file_in:
        with open(temp_path, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)

    return _read_csv_file(temp_path)


def load_edmund_spectrum(
        filter: Literal,
        mode: Literal['t', 'r']
) -> Tuple[np.ndarray, list]:
    """Load an Edmund catalog optic transmission or reflection spectrum from
    the scilightcon database.

    Examples:
        >>> from scilightcon.datasets import load_edmund_spectrum
        >>> data, header = load_edmund_spectrum('lp_450nm')
        >>> np.shape(data)
        (293, 2)
        >>> header
        ['Wavelength (nm)', 'Transmission (%)']

    Args:
        filter (str): `lp_400nm`, `lp_450nm`, `lp_500nm`, `lp_550nm`, `lp_600nm`, `lp_600nm`, `lp_700nm`, `lp_750nm`, `sp_400nm`, `sp_500nm`, `sp_600nm` or `sp_700nm`

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)
        header (List): Column names or empty strings. Shape (n_columns)
    """
    if mode == 't':
        suffix = 'transmission'
    elif mode == 'r':
        suffix = 'reflection'
    else:
        raise ValueError("Invalid mode '{mode}'")

    data_file_name = f'{suffix}_EO_{filter}.csv'

    try:
        data, header = load_csv_data(
            data_file_name=data_file_name,
            data_module=DATA_MODULE_EO
        )
    except FileNotFoundError:
        raise ValueError

    return data, header


def load_hamamatsu_spectrum(
        detector: HamamatsuDetectorName
) -> Tuple[np.ndarray, list]:
    """Load a Hamamatsu detector quantum efficiency spectrum from the
    scilightcon database.

    Examples:
        >>> from scilightcon.datasets import load_hamamatsu_spectrum
        >>> data, header = load_hamamatsu_spectrum('H10721-210')
        >>> np.shape(data)
        (293, 2)
        >>> header
        ['Wavelength (nm)', 'Transmission (%)']

    Args:
        detector (str): `H7422-40`, `H7422-50`, `H10721-01`, `H10721-110`
        or `H10721-210`

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)
        header (List): Column names or empty strings. Shape (n_columns)
    """
    return load_spectrum('hamamatsu', detector)


def load_thorlabs_spectrum(
        filter: ThorlabsFilterName,
        mode: Literal['t', 'r'] = 't'
) -> Tuple[np.ndarray, list]:
    """Load a Thorlabs catalog optic transmission or reflection spectrum from
    the scilightcon database.

    Examples:
        >>> from scilightcon.datasets import load_thorlabs_spectrum
        >>> data, header = load_thorlabs_spectrum('DMLP425')
        >>> np.shape(data)
        (2251, 2)
        >>> header
        ['Wavelength  (nm)', 'Transmission (%)']

    Args:
        filter (str): `DMLP425`, `DMLP550`, `DMLP650`, `FB340-10`, `FBH343-10`,
        `FBH400-40`, `FBH515-10`, `FBH520-40`, `FBH550-40`, `FEL0400`,
        `FEL0450`, `FEL0500`, `FEL0550`, `FEL0600`, `FEL0650`, `FEL0700`,
        `FEL0750`, `FEL0800`, `FEL0850`, `FEL0900`, `FEL0950`, `FEL1000`,
        `FEL1050`, `FEL1100`, `FEL1150`, `FEL1200`, `FEL1250`, `FEL1300`,
        `FEL1350`, `FEL1400`, `FEL1450`, `FEL1500`, `FELH1000`, `FELH1050`,
        `FELH1100`, `FELH1250`, `FELH1500`, `FES0450`, `FES0500`, `FES0550`,
        `FES0600`, `FES0650`, `FES0700`, `FES0750`, `FES0800`, `FES0850`,
        `FES0900`, `FES0950`, `FES1000`, `FESH0450`, `FESH0500`, `FESH0600`,
        `FESH0700`, `FESH0750`,  `FGB37`, `FGB39`, `FGS550`, `FGS700`,
        `FGS900`, `FGUV5`, `FGUV11`, `FL514.5-10`, `FL530-10`, `MF460-60`,
        `NDUV01B`, `NDUV02B`, `NDUV06B`, `NDUV10B`, `NDUV20B`, `NDUV30B`,
        `NDUV40B`, `NE01B`, `NE06B`, `NE10B`, `NE20B`, `NE30B`, `NE40B`,
        `NE50B` or `NE60B`
        mode (str): `t`, `r`

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)
        header (List): Column names or empty strings. Shape (n_columns)
    """
    return load_spectrum('thorlabs', filter, mode)


def load_eksma_spectrum(
    material: EksmaMirrorMaterial
) -> Tuple[np.ndarray, list]:
    """Load an Eksma catalog optic transmission or reflection spectrum from
    the scilightcon database.

    Examples:
        >>> from scilightcon.datasets import load_eksma_spectrum
        >>> data, header = load_eksma_spectrum('Ag')
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
    return load_spectrum('eksma', material)


def load_chroma_spectrum(
        filter: ChromaFilterName,
        mode: Literal['t', 'r'] = 't'
) -> Tuple[np.ndarray, list]:
    """Load a Chroma catalog optic transmission or reflection spectrum from the
    scilightcon database.

    Examples:
        >>> from scilightcon.datasets import load_chroma_spectrum
        >>> data, header = load_chroma_spectrum('ET340X', 't')
        >>> np.shape(data)
        (2251, 2)
        >>> header
        ['Wavelength  (nm)', 'Transmission (%)']

    Args:
        filter (str): `ET340X`
        mode (str): `t`, `r`

    Returns:
        data (Ndarray): A 2D array of data with headers excluded. Shape (n_samples, n_columns)
        header (List): Column names or empty strings. Shape (n_columns)
    """
    return load_spectrum('chroma', filter, mode)

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

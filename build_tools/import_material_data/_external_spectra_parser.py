#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""External spectra importer scripts

Part of scilightcon.

Copyright 2023-2026 Light Conversion
Contact: support@lightcon.com
"""

import re, os, shutil
from pathlib import Path
import pandas as pd
from scipy.io import loadmat
import numpy as np
from typing_extensions import Literal


def thorlabs_xls_to_csv(file_name, mode:Literal['trans', 'refl']):
    """
    Read Thorlabs filter and mirror transmission XLS file and convert to
    a simple CSV file for scilightcon dataset database.

    Limitations:
        - The script only reads the first Excel sheet, usually containing values
        for unpolarized light.

    Usage:
        >>> from _external_spectra_parser import thorlabs_xls_to_csv  # doctest: +SKIP
        >>> wavl, trans = thorlabs_xls_to_csv('DMLP505.xls')  # doctest: +SKIP
    """
    if mode not in ['trans', 'refl']:
        raise ValueError("Mode must be 'trans' or 'refl'")

    print(f"Reading {file_name} for '{mode}' data...")

    # Identify header line by whichever contains the string Wavelength
    # Thorlabs has been using first or second line
    header_line = None
    num_header_test_lines = 5
    preview = pd.read_excel(file_name, header=None, nrows=num_header_test_lines)
    for line_ind in range(num_header_test_lines):
        if preview.iloc[line_ind].astype(str).str.contains('Wavelength', case=False).any():
            header_line = line_ind
            break

    if header_line is None:
        raise RuntimeError("Could not find header line")

    # Find wavelength data column
    header = preview.iloc[header_line]
    wavl_col = None
    for ind, col in enumerate(header):
        if type(col) is str and 'wavelength' in col.lower():
            wavl_col = ind
            break

    if wavl_col is None:
        raise RuntimeError("Could not find wavelength column")

    # Read Excel file
    data = pd.read_excel(file_name, header=header_line, usecols=range(wavl_col, len(header)))

    # Find column indices
    # Assume first column is wavelength in nm
    if not 'wavelength' in data.columns[0].lower():
        raise ValueError("First column is not wavelength")

    if not 'nm' in data.columns[0].lower():
        raise ValueError("Wavelength is not in nm")

    col_ind = []
    for col_ind, col_name in enumerate(data.columns):
        if mode in col_name.lower():
            if not '%' in col_name.lower():
                raise ValueError("Data is not in %")
            break

    if col_ind is None:
        raise RuntimeError(f"Could not find {mode} column")

    wavl = np.array(data.iloc[:, 0], dtype='int')
    ydata = np.array(data.iloc[:, col_ind])

    if mode == 'trans':
        preffix = 'transmission'
        yunits = 'Transmission (%)'
    elif mode == 'refl':
        preffix = 'reflection'
        yunits = 'Reflectance (%)'

    if np.min(wavl < 0):
        raise ValueError("Wavelength < 0")

    if np.max(wavl < 100):
        raise ValueError("Wavelength is probably not in nm")

    if np.min(ydata) < -1:
        raise ValueError("Y data (transmission or reflectance) < 0%")

    if np.max(ydata) < 2:
        raise ValueError("Y data (transmission or reflectance) is probably not in %")

    dataset_file_name = f"{preffix}_THORLABS_{Path(file_name).stem.upper()}.csv"
    print(f"Saving {dataset_file_name}...")
    np.savetxt(dataset_file_name,
            np.transpose([wavl, ydata]),
            header=f"Wavelength  (nm), {yunits}",
            fmt="%.6f",
            delimiter=', ')

    print(f"Copying to datasets...")
    copy_to_datasets(dataset_file_name, folder='Thorlabs')

    return wavl, ydata

def chroma_txt_to_csv(file_name, mode:Literal['trans', 'refl']):
    """
    Read Chroma filter and mirror transmission TXT file and convert to
    CSV file for scilightcon dataset database.

    Limitiations:
        - Chroma spectra files are exported without headers and numeric file names.
        The user must specify correct name and spectra type.

    Usage:
        >>> from _external_spectra_parser import chroma_txt_to_csv  # doctest: +SKIP
        >>> wavl, trans = chroma_txt_to_csv('ET340x.x')  # doctest: +SKIP
    """
    if mode not in ['trans', 'refl']:
        raise ValueError("Mode must be 'trans' or 'refl'")

    print(f"Reading {file_name} assuming it contains '{mode}' data...")

    wavl, ydata = np.loadtxt(file_name, unpack=True)

    if mode == 'trans':
        preffix = 'transmission'
        yunits = 'Transmission (%)'
    elif mode == 'refl':
        preffix = 'reflection'
        yunits = 'Reflectance (%)'

    if np.min(wavl < 0):
        raise ValueError("Wavelength < 0")

    if np.max(wavl < 100):
        raise ValueError("Wavelength is probably not in nm")

    if np.min(ydata) < -1:
        raise ValueError("Y data (transmission or reflectance) < 0%")

    if np.max(ydata) < 2:
        raise ValueError("Y data (transmission or reflectance) is probably not in %")

    dataset_file_name = f"{preffix}_CHROMA_{Path(file_name).stem.upper()}.csv"
    print(f"Saving {dataset_file_name}...")
    np.savetxt(dataset_file_name,
            np.transpose([wavl, ydata]),
            header=f"Wavelength  (nm), {yunits}",
            fmt="%.6f",
            delimiter=', ')

    print(f"Copying to datasets...")
    copy_to_datasets(dataset_file_name, folder='Chroma')

    return wavl, ydata

def edumund_optics_xls_to_csv(file_name, mode:Literal['trans', 'refl']):
    """
    Read EO filter and mirror transmission XLSX file and convert to
    a simple CSV file for scilightcon dataset database.

    Usage:
        >>> from _external_spectra_parser import edmund_optics_xlsx_to_csv  # doctest: +SKIP
        >>> wavl, trans = edmund_optics_xlsx_to_csv('86-337.xlsx')  # doctest: +SKIP
    """
    if mode != 'trans':
        raise RuntimeError("Only transmission Edmund Optics spectra are currently supported")

    print(f"Reading {file_name}...")

    # Edmund Optics uses the following format:
    # CurveName,    	                            XData,  YData,      XColumn,            YColumn
    # HC FL Dichroic Longpass 409nm Transmission,   310,    11.31101,   Wavelength (nm),    Transmission (%)
    # HC FL Dichroic Longpass 409nm Transmission,	311,	13.53099,	Wavelength (nm),	Transmission (%)
    # HC FL Dichroic Longpass 409nm Transmission,	312,	13.15596,	Wavelength (nm),	Transmission (%)


    # Read two lines to check for 'XData' and 'YData' indices and whether XColumn and YColumn contain 'Wavelength (nm)' and 'Transmission (%)'
    preview = pd.read_excel(file_name, header=None, nrows=2)

    # Assuming transmission data
    mode = 'trans'

    # Find wavelength and data columns
    header = preview.iloc[0]
    wavl_col = None
    data_col = None
    for ind, col in enumerate(header):
        if type(col) is not str:
            continue
        if 'xdata' in col.lower():
            wavl_col = ind
        if 'ydata' in col.lower():
            data_col = ind

        val = str(preview.iloc[1, ind]).lower()
        if 'xcolumn' in col.lower():
            if "wavelength" not in val:
                raise RuntimeError("Column not wavelength")
            elif "(nm)" not in val:
                raise RuntimeError("Wavelength not in nm")

        if 'ycolumn' in col.lower():

            if "transmission" not in val:
                raise RuntimeError("Column not transmission")
            elif "(%)" not in val:
                raise RuntimeError("Transmission not in %")

    if wavl_col is None:
        raise RuntimeError("Could not find wavelength column")

    if data_col is None:
        raise RuntimeError("Could not find data column")

    # Read Excel file
    data = pd.read_excel(file_name, header=1, usecols=(wavl_col, data_col))

    wavl = np.array(data.iloc[:, 0])
    ydata = np.array(data.iloc[:, 1])

    if mode == 'trans':
        preffix = 'transmission'
        yunits = 'Transmission (%)'
    elif mode == 'refl':
        preffix = 'reflection'
        yunits = 'Reflectance (%)'

    if np.min(wavl < 0):
        raise ValueError("Wavelength < 0")

    if np.max(wavl < 100):
        raise ValueError("Wavelength is probably not in nm")

    if np.min(ydata) < -1:
        raise ValueError("Y data (transmission or reflectance) < 0%")

    if np.max(ydata) < 2:
        raise ValueError("Y data (transmission or reflectance) is probably not in %")

    dataset_file_name = f"{preffix}_EO_{Path(file_name).stem.upper()}.csv"
    print(f"Saving {dataset_file_name}...")
    np.savetxt(dataset_file_name,
            np.transpose([wavl, ydata]),
            header=f"Wavelength  (nm), {yunits}",
            fmt="%.6f",
            delimiter=', ')

    print(f"Copying to datasets...")
    copy_to_datasets(dataset_file_name, folder='EO')

    return wavl, ydata


def emitter_txt_to_csv(file_name, mode:Literal['ex', 'em', '2pex']):
    """
    Read a generic fluorophore/luminophore excitation or emission spectrum TXT
    file and convert to CSV file for scilightcon dataset database.

    Usage:
        >>> from _external_spectra_parser import emitter_txt_to_csv  # doctest: +SKIP
        >>> wavl, trans = emitter_txt_to_csv('ET340x.x')  # doctest: +SKIP
    """
    file_name = Path(file_name)
    if mode not in ['ex', 'em', '2pex']:
        raise ValueError("Mode must be 'ex', 'em' or '2pex'")

    print(f"Reading {file_name} assuming it contains '{mode}' data...")

    name = file_name.stem.upper().split('-')[0]
    print(f"Using '{name}' as emitter name")

    wavl, ydata = np.loadtxt(file_name, unpack=True)

    if mode == 'ex':
        preffix = 'ex'
        yunits = 'Excitation (a.u.)'
    elif mode == '2pex':
        preffix = '2pex'
        yunits = '2P Excitation (a.u.)'
    elif mode == 'em':
        preffix = 'em'
        yunits = 'Emission (a.u.)'

    if np.min(wavl < 0):
        raise ValueError("Wavelength < 0")

    if np.max(wavl < 100):
        raise ValueError("Wavelength is probably not in nm")

    if np.min(ydata) < -1:
        raise ValueError("Y data less than 0")

    if np.max(ydata) < 2:
        raise ValueError("Y data is probably not normalized to 100")

    dataset_file_name = f"{name}_{preffix}.csv"
    print(f"Saving {dataset_file_name}...")
    np.savetxt(dataset_file_name,
            np.transpose([wavl, ydata]),
            header=f"Spectrum from '{file_name.stem}'\nWavelength  (nm), {yunits}",
            fmt="%.6f",
            delimiter=', ')

    print(f"Copying to datasets...")
    copy_to_datasets(dataset_file_name, folder='Emitters')

    return wavl, ydata



def copy_to_datasets(file_name: Path|str, folder:Literal['Thorlabs', 'Hamamatsu', 'EO', 'Chroma', 'Emitters']) -> bool:
    """
    Copy a CSV file to scilightcon dataset folder.
    """
    if folder is not None and folder.lower() not in ['thorlabs', 'hamamatsu', 'eo', 'chroma', 'emitters']:
        raise ValueError("Folder must be 'Thorlabs', 'Hamamatsu', 'EO', 'Chroma or 'Emitters'")

    file_name = Path(file_name)

    if file_name.suffix != '.csv':
        raise ValueError("File must be CSV")

    target_file_path = Path("../../scilightcon/datasets/data") / folder.lower() / file_name

    if os.path.isfile(target_file_path):
        print(f"File '{file_name}' already exists in database, skipping")
        return False

    chunks = str(file_name.stem).split('_')
    if folder == 'Emitters':
        if len(chunks) != 2:
            raise ValueError("File name format must be <name>_<mode>.csv")
        name = chunks[0]
    else:
        if len(chunks) != 3:
            raise ValueError("File name format must be <mode>_<folder>_<name>.csv")
        name = chunks[2]

        if chunks[0] not in ['reflection', 'transmission', 'qe']:
            raise ValueError("Mode must be 'reflection', 'transmission' or 'qe'")

        if chunks[1].lower() not in ['thorlabs', 'hamamatsu', 'eo', 'chroma']:
            raise ValueError(f"Folder ('{chunks[1]}') must be 'Thorlabs', 'Hamamatsu', 'EO', or 'Chroma'")

    if re.compile(r'[A-Z0-9-]+').fullmatch(name) is None:
        raise ValueError("Name can only contain: uppercase latin letters, numbers and the minus character")

    shutil.copy2(file_name, target_file_path)

    return True


def matlab_fig_to_csv(file_name):
    data = loadmat(file_name, squeeze_me=True, struct_as_record=False)

    curve_data = []
    for child in data['hgS_070000'].children[0].children:
        if child.type == 'graph2d.lineseries':
            name = child.properties.DisplayName
            xdata = child.properties.XData
            ydata = child.properties.YData

            print(f"Found curve '{name}', data len: {len(xdata)}")

            dataset_file_name = f"qe_Hamamatsu_{name}.csv"
            np.savetxt(dataset_file_name,
                       np.transpose([xdata, ydata]),
                       header="Wavelength  (nm), QE (%)",
                       fmt="%.6f",
                       delimiter=', ')

            copy_to_datasets(dataset_file_name, folder='Hamamatsu')

            curve_data.append([xdata, ydata, name])

    return curve_data

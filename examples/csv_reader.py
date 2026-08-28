#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example: load Argon line spectra

Part of scilightcon.

Copyright 2023-2026 Light Conversion
Contact: support@lightcon.com
"""
import csv
import numpy as np
from importlib.resources import files

csv_filepath = str(files('scilightcon').joinpath("datasets/data/Ar_lines.csv"))

with open(csv_filepath, 'r') as csv_file:
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

    print (data)
    print (header)
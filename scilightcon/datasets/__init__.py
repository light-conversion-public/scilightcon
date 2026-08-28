#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dataset loading module

Part of scilightcon.

Copyright 2023-2026 Light Conversion
Contact: support@lightcon.com
"""

from ._base import load_thorlabs_spectrum, load_edmund_spectrum, \
    load_chroma_spectrum , load_eksma_spectrum, load_hamamatsu_spectrum, \
    load_spectrum, \
    load_csv_data, load_zipped_csv_data, \
    load_atmospheric_data, DATA_MODULE
from ._logs_reader import LogsReader

__all__ = [
    "load_thorlabs_spectrum",
    "load_edmund_spectrum",
    "load_chroma_spectrum",
    "load_eksma_spectrum",
    "load_hamamatsu_spectrum",
    "load_spectrum",
    "load_csv_data",
    "load_zipped_csv_data",
    "load_atmospheric_data",
    "load_csv_data",
    "LogsReader"
]

_materials = _base.load_materials()

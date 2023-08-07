"""Module for loading datasets"""

from ._base import load_EKSMA_OPTICS_mirror_reflections, load_EO_filter_transmissions, load_THORLABS_filter_transmissions, load_csv_data, load_zipped_csv_data, load_atmospheric_data, DATA_MODULE
from ._logs_reader import LogsReader

__all__ = [
    "load_EKSMA_OPTICS_mirror_reflections",
    "load_EO_filter_transmissions",
    "load_THORLABS_filter_transmissions",
    "load_csv_data",
    "load_zipped_csv_data",
    "load_atmospheric_data",
    "load_csv_data",
    "LogsReader"
]

_materials = _base.load_materials()

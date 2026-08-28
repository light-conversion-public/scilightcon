"""A set of useful functions"""

from ._interpolate_and_multiply import interpolate_and_multiply, _interpolate_and_multiply_ndarray, _interpolate_and_multiply_list
from ._constants import c
from ._analyze_s2_data import load_s2s_data, ShotToShotData, ShotToShotOutlier

__all__ = [
    "interpolate_and_multiply",
    "_interpolate_and_multiply_ndarray",
    "_interpolate_and_multiply_list",
    "load_s2s_data",
    "c",
    "ShotToShotData",
    "ShotToShotOutlier",
    ] 
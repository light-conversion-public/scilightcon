"""A set of useful functions"""

from ._interpolate_and_multiply import interpolate_and_multiply
from ._analyze_s2_data import load_s2s_data, ShotToShotData, ShotToShotOutlier

__all__ = [
    "interpolate_and_multiply",
    "load_s2s_data",
    "ShotToShotData",
    "ShotToShotOutlier",
] 
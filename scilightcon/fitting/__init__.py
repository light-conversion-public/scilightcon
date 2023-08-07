"""Module for data fitting routines"""

from ._detect_peaks import detect_peaks
from ._fitting_2d_beam_profiles import fit_beam_profile_2d

__all__ = [
    "detect_peaks",
    "fit_beam_profile_2d"       
]
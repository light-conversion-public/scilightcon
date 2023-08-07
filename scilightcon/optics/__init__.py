"""Module for calculating optical parameters"""

from ._materials import load_material, Material
from ._spectra import get_Hg_spectrum
from ._spectra import get_Ar_spectrum
from ._spectra import get_White_LED_spectrum

__all__ = [
    "load_material",
    "Material",
    "get_Hg_spectrum",
    "get_Ar_spectrum",
    "get_White_LED_spectrum"
]
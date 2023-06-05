"""Module for calculating optical parameters"""

from ._materials import load_material, Material

__all__ = [
    "Material",
    "load_material",
]
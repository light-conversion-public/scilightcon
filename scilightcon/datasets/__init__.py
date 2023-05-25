"""Module for loading datasets"""

from ._base import load_EKSMA_OPTICS_mirror_reflections, load_materials

__all__ = [
    "load_EKSMA_OPTICS_mirror_reflections",
    "load_materials"
]

_materials = load_materials()
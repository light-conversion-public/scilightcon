#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Interpolate and multiply helper function

Part of scilightcon.

Copyright 2023-2026 Light Conversion
Contact: support@lightcon.com
"""

from scipy.interpolate import interp1d
import numpy as np
from typing import Tuple, List

def _interpolate_and_multiply_list(
        arr1: Tuple[List[float], List[float]],
        arr2: Tuple[List[float], List[float]]) -> Tuple[List[float], List[float]] :
    """Interpolate an X,Y arr2 so that it has the same X as arr1.

    Tuple of lists implementation. See `interpolate_and_multiply()` for details.
    """
    x2 = arr2[0]
    y2 = arr2[1]
    interp_func = interp1d(x2, y2, bounds_error=False, fill_value=np.nan)

    x1 = arr1[0]
    y1 = arr1[1]
    y2_interp = interp_func(x1)

    valid_indices = np.logical_not(np.logical_or(np.isnan(arr1[0]), np.isnan(y2_interp)))

    return (list(np.array(x1)[valid_indices]), list(np.array(y1)[valid_indices]) * np.array(y2_interp)[valid_indices])


def _interpolate_and_multiply_ndarray(
        arr1: np.ndarray,
        arr2: np.ndarray) -> np.ndarray:
    """Interpolate an X,Y arr2 so that it has the same X as arr1.

    ndarray implementation. See `interpolate_and_multiply()` for details.
    """
    interp_func = interp1d(arr2[:,0], arr2[:,1], bounds_error=False, fill_value=np.nan)
    y2_interp = interp_func(arr1[:,0])
    valid_indices = np.logical_not(np.logical_or(np.isnan(arr1[:,0]), np.isnan(y2_interp)))

    return np.column_stack([arr1[valid_indices,0], arr1[valid_indices,1]*y2_interp[valid_indices]])

def interpolate_and_multiply(
        arr1: np.ndarray | Tuple[List[float], List[float]],
        arr2: np.ndarray | Tuple[List[float], List[float]]) -> np.ndarray | Tuple[List[float], List[float]] :
    """Interpolate an X,Y arr2 so that it has the same X as arr1.

    `arr1` and `arr2` can be np.ndarray or Tuple.

    Args:
        arr1 (ndarray or tuple): Reference array
        arr2 (ndarray or tuple): Array to be interpolated

    Returns:
        Interpolated X,Y array in the same type as arr1.
    """
    if type(arr1) == Tuple and type(arr2) == Tuple:
        return _interpolate_and_multiply_list(arr1, arr2)
    elif type(arr1) == np.ndarray and type(arr2) == np.ndarray:
        return _interpolate_and_multiply_ndarray(arr1, arr2)
    else:
        raise RuntimeError(f"Unhandled array type combination {type(arr1)} {type(arr2)}")


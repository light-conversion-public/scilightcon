import numpy as np
import csv
from typing import List
from scilightcon.datasets import load_csv_data

def get_Hg_spectrum(wl, width) -> float:
    data, header = load_csv_data('Hg_lines.csv')
    wl_lines = data[:,0]
    I_lines = data[:,1]    
    
    return  _get_spectrum_from_lines(wl_lines, I_lines, wl, width)

def get_Ar_spectrum(wl, width) -> float:
    data, header = load_csv_data('Ar_lines.csv')
    wl_lines = data[:,0]
    I_lines = data[:,1]    
    
    return  _get_spectrum_from_lines(wl_lines, I_lines, wl, width)

def get_White_LED_spectrum(wl, width) -> float:
    data, header = load_csv_data('White_LED_spectrum.csv')
    wl_lines = data[:,0]
    I_lines = data[:,1]    
    
    return  _get_spectrum_from_lines(wl_lines, I_lines, wl, width)

def _get_spectrum_from_lines(wl_lines: List [float], I_lines: List[float], wl : float, width : float) -> float:

    spectrum = np.sum(I_line * np.exp(-(wl-wl_line)**2 /(2*width**2)) 
                   for wl_line, I_line in zip(wl_lines, I_lines))

    return spectrum

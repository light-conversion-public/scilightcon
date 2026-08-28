#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MATLAB Fig to CSV Example for Hamamatsu PMT QE curves

Part of scilightcon.

Copyright 2023-2026 Light Conversion
Contact: support@lightcon.com
"""
from _external_spectra_parser import matlab_fig_to_csv
import matplotlib.pyplot as plt

if __name__ == '__main__':
        file_name = 'hamamatsu_pmt_qe.fig'
        curve_data = matlab_fig_to_csv(file_name)
        for curve in curve_data:
            plt.plot(curve[0], curve[1], label=curve[2])

        plt.xlabel('Wavelength')
        plt.ylabel('QE')
        plt.legend()
        plt.grid(True)
        plt.show()


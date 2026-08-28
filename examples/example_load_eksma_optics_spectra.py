#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example: load EKSMA Optics mirror spectra.

Part of scilightcon.

Copyright 2023-2026 Light Conversion
Contact: support@lightcon.com
"""
from scilightcon.datasets import load_eksma_spectrum
import matplotlib.pyplot as plt

plt.figure()

for material in ['Au', 'Ag', 'Al']:
    data, headers = load_eksma_spectrum(material)
    plt.plot(data[:,0], data[:,1], label = material)

plt.xlabel(headers[0])
plt.ylabel(headers[1])
plt.legend()
plt.grid(True)

plt.show()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# 
#--------------------------------------------------------------------------
# Copyright (c) 2020 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
import matplotlib.pyplot as plt
import numpy as np
import scilightcon
import pickle
from scilightcon.utils._fixes import _open_binary

from scilightcon.plot import apply_style, reset_style, add_watermark, add_watermarks
    
def _get_sample_beam_profile():
    _yc = 74
    _xc = 102
    _pixel_size = 45.40
    filepath =  _open_binary(scilightcon.datasets.DATA_MODULE, 'test_beam_profile.pkl')
    _matrix = pickle.load(filepath)['matrix']
    
    return {'matrix' : _matrix,
            'pixel_size': _pixel_size,
            'xc': _xc,
            'yc': _yc,
            'yaxis': (np.arange(_matrix.shape[0]) - _yc) * _pixel_size,
            'xaxis': (np.arange(_matrix.shape[1]) - _xc) * _pixel_size}

fignames = ['example_plot_style_default', 'example_plot_style_scilightcon', 'example_plot_style_scilightcon_one_watermark', 'example_plot_style_scilightcon_watermarks']

for figname in fignames:
    if 'default' in figname:
        reset_style()
        cmaps = ['viridis', 'viridis']
    else:
        apply_style()
        cmaps = ['RdYlGnBu', 'beam_profile']

    plt.figure(figname, figsize=(8, 8))
    plt.clf()
    fig, axes = plt.subplots(2, 2, squeeze=True, gridspec_kw = {'height_ratios': [3, 4], 'width_ratios': [3,4]}, num=figname)

    ax1 = axes[0,0]
    ax2 = axes[0,1]
    ax3 = axes[1,0]
    ax4 = axes[1,1]

    # FITS 
    x = np.arange(100)
    ax1.plot(x, np.exp(-x / 10) + np.random.randn(len(x))*0.1, label = 'function')
    ax1.plot(x, np.exp(-x / 10), label = 'fit')

    ax1.set_xlabel('Something, fs')
    ax1.set_ylabel('Something else, V')
    ax1.set_title('Fit of function')
    ax1.legend()

    # MANY LINES
    x = np.arange(10)
    for i in np.arange(10):
        ax2.plot(x, x*i/10 + i + 1 + np.random.randn(len(x)) * 0.1, '.-', label='{:}'.format(i+1))

    ax2.set_ylim([0,None])
    ax2.set_xlabel('Something, fs')
    ax2.set_ylabel('Something else, V')
    ax2.set_title('Many curves')
    ax2.legend()

    # 2D CHART
    x = np.arange(-3.0, 3.0, 0.01)
    y = np.arange(-3.0, 3.0, 0.01)

    xx,yy = np.meshgrid(x, y)

    z = np.exp(-xx**2) * np.exp(-yy**2) * np.sin(yy)
            
    absmax = np.max(np.abs(z))


    im = ax3.imshow(z, vmin=-absmax, vmax=absmax,  extent=[-1, 1, -1, 1], cmap=cmaps[0])
    cbar = plt.colorbar(im,  ax=ax3, orientation='horizontal')
    cbar.ax.tick_params(labelsize=8)
    ax3.grid(False)

    ax3.set_xlabel('X, mm')
    ax3.set_ylabel('Y, mm')
    ax3.set_title('2D graph')

    # SHADED REGION
    info = _get_sample_beam_profile()

    bp = ax4.imshow(info['matrix'], extent = [info['xaxis'][0], info['xaxis'][-1], info['yaxis'][-1], info['yaxis'][0]], cmap=cmaps[1])

    ax4.set_title('Beam profile')
    ax4.set_xlabel('X, um')
    ax4.set_ylabel('Y, um')

    cbar = plt.colorbar(bp,  ax=ax4, orientation='horizontal')
    cbar.ax.tick_params(labelsize=8)

    ax4.grid(False)

    if 'one_watermark' in figname:
        add_watermark(fig)
    if 'watermarks' in figname:
        add_watermark(ax1)
        add_watermark(ax2)
        add_watermark(ax3)
        add_watermark(ax4)

    plt.tight_layout()

    plt.draw()

    plt.savefig(f'./doc/docs/img/{figname}.png')


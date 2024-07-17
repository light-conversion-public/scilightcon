import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
from ._fixes import resize_mode

import os
import numpy as np
from pathlib import Path
from matplotlib import rcParams

available_wm_widths = np.array([100, 150, 300, 800, 1200])
wm_min_ratio_axis = 0.3
wm_min_ratio_figure = 0.5
wm_alpha = 0.2

_gradient_stops_RdYlGnBu = [(0.000,(0xDA,0x70,0xD6)),
                  (0.250,(0x00,0x00,0xFF)),
                  (0.500,(0xFF,0xFF,0xFF)),
                  (0.625,(0x31,0x87,0x15)),
                  (0.750,(0xFE,0xF9,0x00)),
                  (0.875,(0xFF,0x00,0x00)),
                  (1.000,(0xA5,0x2A,0x2A))
                   ]

_gradient_stops_beam_profile = [(0.0, (0x00,0x3A,0x7E)),
                           (0.2, (0x64,0x95,0xED)),
                           (0.4, (0x00,0x64,0x00)),
                           (0.6, (0x7f,0xff,0x00)),
                           (0.8, (0xff,0xff,0x00)),
                           (1.0, (0xff,0x00,0x00))]

_gradient_stops_morgenstemning = [(0.0, (0x00,0x00,0x00)),
                                  (0.1, (0x05,0x1B,0x2A)),
                                  (0.2, (0x13,0x31,0x55)),
                                  (0.3, (0x50,0x31,0x72)),
                                  (0.4, (0xA0,0x21,0x73)),
                                  (0.5, (0xA0,0x21,0x73)),
                                  (0.6, (0xE0,0x3E,0x5F)),
                                  (0.7, (0xF7,0xA6,0x22)),
                                  (0.8, (0xFC,0xEF,0x1B)),
                                  (0.9, (0xFF,0xFE,0x9F)),
                                  (1.0, (0xFF,0xFF,0xFF))]

_gradient_stops_LCBeamProfiler = [(0.0/9.0,  (0x00,0x00,0x00)),#black
                  (1.0/9.0,   (0x32,0x32,0x32)),#dark blue
                  (2.0/9.0,   (0x00,0x00,0xff)),#cyan 
                  (3.0/9.0,   (0x00,0xc0,0xff)),#dark green
                  (4.0/9.0,   (0x3c,0xb4,0x70)),#green
                  (5.0/9.0,   (0x7f,0xff,0x00)),#yellow
                  (6.0/9.0,   (0xff,0xff,0x00)),#red
                  (7.0/9.0,   (0xff,0x00,0x00)),#dark red
                  (8.0/9.0,   (0xff,0x12,0x95)),#magenta
                  (9.0/9.0,   (0xff,0xf0,0xfb))]

    
def _register_colormaps():            
    cmap_info = [('RdYlGnBu', _gradient_stops_RdYlGnBu, 256),
                 ('beam_profile', _gradient_stops_beam_profile, 256),
                 ('LCBeamProfiler', _gradient_stops_LCBeamProfiler, 256),
                 ('morgenstemning', _gradient_stops_morgenstemning, 256)]
    
    for name,gradient_stops,ncols in cmap_info:        
        palette0 = np.zeros((ncols,3))
    
        i_stop = 0
        for i in np.arange(ncols):
            val = i/ncols
            if gradient_stops[i_stop+1][0] < val:
                i_stop = i_stop + 1
            x1 = gradient_stops[i_stop][0]
            x2 = gradient_stops[i_stop+1][0]
            c1 = gradient_stops[i_stop][1]
            c2 = gradient_stops[i_stop+1][1]
            
            for j in np.arange(3):
                palette0[i][j] = (c1[j] + (val - x1) / (x2 - x1) * (c2[j] - c1[j]))/256.0
                
        try:
            if hasattr(mpl.colormaps, 'get_cmap'):
                val = mpl.colormaps.get_cmap(name)
            else:
                val = mpl.cm.get_cmap(name)
        except ValueError:     
            pass
        cmap = LinearSegmentedColormap.from_list(name, palette0)
        # creg = matplotlib.cm.ColormapRegistry()
        try:
            if hasattr(mpl.colormaps, 'register'):
                mpl.colormaps.register(cmap, name=name)
            else:
                mpl.cm.register_cmap(name, cmap)
        except ValueError:
            pass

def apply_style():
    """Applies the Light Conversion stylesheet and load additional colormaps (`RdYlGnBu`, `beam_profile`, `LCBeamProfiler`, `morgenstemning`) to matplotlib"""
    stylesheet_path = os.path.join(str(Path(__file__).parent), 'lcstyle.mplstyle')

    _register_colormaps()

    mpl.style.use('default')
    mpl.style.use(stylesheet_path)
    
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Source Sans Pro', 'Arial', 'cmss10']
    
def reset_style():
    """Applies the default matplotlib stylesheet"""
    mpl.style.use('default')

def _determine_logo_width(target_width, ratio, use_larger = True):
    out_width = None
    if use_larger:
        avails = available_wm_widths[available_wm_widths > target_width * ratio]
        out_width = target_width * ratio if len(avails)==0 else avails[0]
    else:
        avails = available_wm_widths[available_wm_widths < target_width * ratio]
        out_width = target_width * ratio if len(avails)==0 else avails[::-1][0]
    
    if out_width > target_width and use_larger:        
        return _determine_logo_width(target_width, ratio, use_larger = False)
    else:
        return out_width    

def add_watermarks(fig : plt.Figure):
    """Adds watermarks to all subplots of given figure
    
    Args:
        fig (plt.Figure): Figure object (use `plt.gcf()` for current figure)
    """
    for ax in fig.axes:
        add_watermark(ax)

def add_watermark(target, loc='lower left'):
    """Add watermark to current axis or figure

    Args:
        target (plt.Axes, plt.Figure): Axis or Figure object
        loc (str): Location of the watermark (`upper right`|`upper left`|`lower left`|`lower right`|`center left`|`center right`|`lower center`|`upper center`|`center`).
            Default value is `center` when `target` is `figure` and `lower left` for `target` is `axis`
    """
    from PIL import Image
    from matplotlib.offsetbox import ( OffsetImage,AnchoredOffsetbox)

    file_name = (str)(Path.joinpath(Path(__file__).parent, 'lclogo.png'))
    img = Image.open(file_name)
    
    if isinstance(target, plt.Axes):
        ax = target
        fig = ax.get_figure()
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width = bbox.width * fig.dpi
        
        wm_width = int(_determine_logo_width(width, wm_min_ratio_axis))                       # make watermark larger than given ratio
        scaling = (wm_width / float(img.size[0]))
        wm_height = int(float(img.size[1])*float(scaling))
        img = img.resize((wm_width, wm_height), resize_mode())
    
        imagebox = OffsetImage(img, zoom=1, alpha=wm_alpha)
        imagebox.image.axes = ax
    
        ao = AnchoredOffsetbox(loc, pad=0.5, borderpad=0, child=imagebox)
        ao.patch.set_alpha(0)
        ax.add_artist(ao)

    if isinstance(target, plt.Figure):
        fig = target
        bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width, height = fig.get_size_inches() * fig.dpi
        
        wm_width = int(_determine_logo_width(width, wm_min_ratio_figure, use_larger=True))    # make watermark smaller than given ratio
        scaling = (wm_width / float(img.size[0]))
        wm_height = int(float(img.size[1])*float(scaling))
        
        img = img.resize((wm_width, wm_height), resize_mode())
        
#        if loc == 'center':
        logo_pos = [(fig.bbox.xmax - wm_width)/2, (fig.bbox.ymax - wm_height)/2]

        
        fig.figimage(img, logo_pos[0], logo_pos[1], alpha=wm_alpha)
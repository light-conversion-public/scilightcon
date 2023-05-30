#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# 
#--------------------------------------------------------------------------
# Copyright (c) 2021 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
import numpy as np
import scilightcon
from scilightcon.utils import load_s2s_data

from importlib import resources

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 100000000

s_duration = 1
m_duration = 100
sml_ylim = [0.95, 1.05]
nrmsd_ylim = [0, 1.0]

filepath = resources.files(scilightcon.datasets.DATA_MODULE).joinpath('Shot-to-shot_LAB4 PHAROS_25.0kHz_1030nm_InGaAs_20210917_1337.s2s')

s2s_data = load_s2s_data(filepath)

if s2s_data.version == 1:
    
    if s2s_data.sml_data is not None:    
        plt.figure('Pulse energy of ' + s2s_data.device_serial_number)
        plt.clf()
        plt.suptitle('Energy stability of {:}, {:.1f} kHz, {:.0f} nm'.format(s2s_data.device_serial_number, s2s_data.repetition_rate, s2s_data.wavelength))
        
        plt.subplot(311)    
        saxis = np.arange(0, s_duration * s2s_data.repetition_rate)
        sdata = s2s_data.sml_data[0:len(saxis)]
        plt.plot(saxis / s2s_data.repetition_rate, sdata, label = '{:.3f} % NRMSD'.format(np.std(sdata)/np.mean(sdata)*100))
        plt.xlabel('Time, ms')
        plt.ylabel('Pulse energy, a.u.')
        plt.legend()
        plt.ylim(sml_ylim)
        
        plt.subplot(312)    
        maxis = np.arange(0, m_duration * s2s_data.repetition_rate)
        mdata = s2s_data.sml_data[0:len(maxis)]
        plt.plot(maxis / s2s_data.repetition_rate, mdata, label = '{:.3f} % NRMSD'.format(np.std(mdata)/np.mean(mdata)*100))
        plt.xlabel('Time, ms')
        plt.ylabel('Pulse energy, a.u.')
        plt.legend()
        plt.ylim(sml_ylim)
        
        plt.subplot(313)    
        laxis = np.arange(0, len(s2s_data.sml_data))    
        plt.plot(laxis / s2s_data.repetition_rate / 1000, s2s_data.sml_data, label = '{:.3f} % NRMSD'.format(np.std(s2s_data.sml_data)/np.mean(s2s_data.sml_data)*100))
        plt.xlabel('Time, s')
        plt.ylabel('Pulse energy, a.u.')
        plt.legend()
        plt.ylim(sml_ylim)
        
    if s2s_data.nmrsd_data_y is not None:
        plt.figure('NRMSD of ' + s2s_data.device_serial_number)
        plt.clf()
        plt.suptitle('NRMSD of {:}, {:.1f} kHz, {:.0f} nm'.format(s2s_data.device_serial_number, s2s_data.repetition_rate, s2s_data.wavelength))
        
        plt.plot((np.array(s2s_data.nmrsd_data_x) - s2s_data.nmrsd_data_x[0]) * 60, s2s_data.nmrsd_data_y)
        plt.xlabel('Time, s')
        plt.ylabel('Normalize root-mean-square deviation, %')
        plt.ylim(nrmsd_ylim)
    
    if s2s_data.outliers is not None:
        fig = plt.figure('Outliers of ' + s2s_data.device_serial_number)
        plt.clf()
        plt.suptitle('Outliers of ' + s2s_data.device_serial_number)
        fig.subplots_adjust(hspace=0)
        n = len(s2s_data.outliers)
        
        vmax = np.max([np.max(outlier.voltage) for outlier in s2s_data.outliers])
        vmin = np.min([np.min(outlier.voltage) for outlier in s2s_data.outliers])
        if vmax < s2s_data.sml_mean:
            vmax = s2s_data.sml_mean * 1.01
            
        if vmin > s2s_data.sml_mean:
            vmin = s2s_data.sml_mean * 0.99
                        
        for i, outlier in enumerate(s2s_data.outliers):
            ax = plt.subplot(n, 1, i+1)            
                                    
            plt.plot(outlier.voltage, label = 'at {:.0f} s'.format((outlier.time - s2s_data.nmrsd_data_x[0]) * 60))
            plt.plot([0, len(outlier.voltage)], [s2s_data.sml_mean, s2s_data.sml_mean])            
            plt.ylim([vmin, vmax])
                        
            plt.ylabel('Voltage, V')
            plt.legend()
                
            if (i+1 < len(s2s_data.outliers)):
                ax.set_xticklabels([])
        ax.set_xlabel('Sample')
            
        
        
        plt.figure('FFT of outliers of ' + s2s_data.device_serial_number)
        plt.clf()
        plt.suptitle('FFT of outliers of ' + s2s_data.device_serial_number)
        
        for i, outlier in enumerate(s2s_data.outliers):
            ax = plt.subplot(n, 1, i+1)       
        
            m = len(outlier.voltage)
            st = int(m/s2s_data.repetition_rate * 0.5)
            ffty = np.abs(np.fft.fft(outlier.voltage))
            fftx = np.fft.fftfreq(len(ffty), 1.0 / s2s_data.repetition_rate)
            
            plt.plot(fftx[st:int(m/2-1)], ffty[st:int(m/2-1)])

            if (i+1 < len(s2s_data.outliers)):
                ax.set_xticklabels([])
        ax.set_xlabel('Frequency, kHz')

plt.show()
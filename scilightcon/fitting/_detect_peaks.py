from typing import List, Tuple
import numpy as np

def detect_peaks(x : List[float], y : List[float], method : str, n_max : int, options = {}) -> List[Tuple[int,int]]:
    """  
        Peak detection function using different algorithms.

        Examples:
            >>> from scilightcon.datasets import load_csv_data
            >>> fname = 'data_test_detect_peaks.csv'
            >>> data, header = load_csv_data(fname)
            >>> x = data[:,0]
            >>> y = data[:,1]
            >>> method = "above_average"
            >>> clusters = detect_peaks(x, y, method = method, n_max=2)
            >>> print('clusters', clusters)
            clusters [[22, 25], [12, 15]]

        Args:
            x (float): x axis data  
            y (float): y axis data
            method (str): [`above_average`, `z_score`, `dispersion`]
            n_max (int): Maximum number of peaks
            options (dict): Additional options to pass to the chosen algorithm

        Returns:
            A list of tuples indicating the begining and the end of peaks       
        """
    if method == 'above_average':
        detected_peaks=_algorithm_ae(x, y)
    elif method == 'z_score': 
        detected_peaks=_algorithm_zscore(x, y, z_score = options.get('z_score'))
    elif method == 'dispersion':
        detected_peaks=_algorithm_dispersion(x, y)
    else:
        raise ValueError (f'Invalid method')

    return _analyze_clusters(y, detected_peaks, n_max)

def _algorithm_ae(x,y):
    avg = np.average(y)
    return np.array([1.0 if item > avg else 0.0 for item in y])

def _algorithm_zscore(x,y, z_score = None):
    z_score = z_score or 0.3
    avg = np.average(y)
    std = np.std(y)
    return np.array([1.0 if np.abs(item - avg) > std * z_score else 0.0 for item in y])

def _algorithm_dispersion(x, y):    
    lag = 100
    if lag > len(x):
        lag = int(len(x)/2)
    threshold = 3.0
    influence = 0.0
#    find minimum of stds of lag length
    stds = [np.std(y[i:(i+lag)]) for i in np.arange(0, len(y)-lag)]
    i_start = np.argmin(stds)
    y_peak = np.zeros((len(y)))
    signal = np.roll(y[:], -i_start)
    y_processed = signal[0:lag]
    for i in np.arange(lag, len(signal)):
        y_val = signal[i]
        avg = np.average(y_processed[(i-lag):i])
        std = np.std(y_processed[(i-lag):i])
        if np.abs(y_val - avg) > std * threshold:
            y_peak[i] = 1.0
            y_processed = np.append(y_processed, (influence * y_val) + (1.0 - influence) * y_processed[i-1])
        else:
            y_processed = np.append(y_processed, [y_val])
    return np.roll(y_peak, i_start)

def _analyze_clusters(y, y_peak, n_max):
    clusters = []
    for i in np.arange(len(y)-1):
        if (y_peak[i]==1.0 and i==0) or (y_peak[i]==0.0 and y_peak[i+1]!=0.0):
            clusters = clusters + [[i,0]]
        if (y_peak[i]==1.0 and i==(len(y)-2)) or (y_peak[i]!=0.0 and y_peak[i+1]==0.0):
            clusters[-1][1] = i
    n_clusters = len(clusters)
    cluster_avgs = [np.abs(np.sum(y[(span[0]):(span[1])])) for span in clusters]
    cluster_max_args = np.argsort(cluster_avgs)[::-1]

    clusters = [clusters[cluster_max_args[i]] for i in np.arange(np.min([n_max, n_clusters]))]
    return clusters
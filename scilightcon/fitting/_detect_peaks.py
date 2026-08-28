from typing import List, Tuple
import numpy as np

def detect_peaks(x : List[float], y : List[float], method : str, n_max: int=None, options = {}) -> List[Tuple[int,int]]:
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
            method (str): [`above_average`, `z_score`, `dispersion`, `clusters`]
            n_max (int): Maximum number of peaks
            options (dict): Additional options to pass to the chosen algorithm

        Returns:
            A list of tuples indicating the beginning and the end of regions
            each containing a detected peak.

        Algorithms:
            - above_average: peaks where signal is above average
                Options:
                    - avg (float): custom average value, default: average of all y values
            - z_score: peaks where signal deviates from average by a given
                z-score which is a fraction of standard deviation (default: 0.3)
                Options:
                    - z_score (float): z-score threshold, default: 0.3
            - dispersion: TBU
        """
    if method == 'above_average':
        detected_peaks=_algorithm_ae(x, y, avg=options.get('avg'))
    elif method == 'z_score':
        detected_peaks=_algorithm_zscore(x, y, z_score=options.get('z_score'))
    elif method == 'dispersion':
        detected_peaks=_algorithm_dispersion(x, y)
    else:
        raise ValueError (f'Invalid method')

    return _analyze_clusters(y, detected_peaks, n_max)

def _algorithm_ae(x, y, avg=None):
    avg = avg or np.average(y)
    return np.array([1.0 if item > avg else 0.0 for item in y])

def _algorithm_zscore(x,y, z_score=None):
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

def _analyze_clusters(y, y_peak, n_max=None):
    """Determine peak regions by analyzing clusters of detected peak points.

    Peak regions are defined as contiguous sequences of points where peaks
    are detected in y_peak. Each region is represented by a [from, to] index
    tuple.

    If `n_max` is specified and the number of detected peaks is larger than
    n_max, only n_max largest peaks are returned.

        Args:
            y (float arr): noisy data with peaks
            y_peak (float arr): binary mask where peaks are detected
            n_max (int): maximum number of peaks to return or None to return all

        Returns:
            A list of [from, to] index tuples where a peak is found in y, up to
            n_max peaks.
    """
    clusters = []

    # Find peak regions in y_peak mask
    for i in np.arange(len(y)-1):
        # If a mask starts with a high value, or there's a transition from low
        # to high, start a new cluster
        if (y_peak[i]==1.0 and i==0) or (y_peak[i]==0.0 and y_peak[i+1]!=0.0):
            clusters = clusters + [[i,0]]

        # If a mask ends with a high value, or there's a transition from high
        # to low, end the current cluster
        if (y_peak[i]==1.0 and i==(len(y)-2)) or (y_peak[i]!=0.0 and y_peak[i+1]==0.0):
            clusters[-1][1] = i

    # Sort clusters by by peak height
    n_clusters = len(clusters)
    cluster_avgs = [np.abs(np.sum(y[(span[0]):(span[1])])) for span in clusters]
    cluster_max_args = np.argsort(cluster_avgs)[::-1]

    if n_max:
        # Return only the n_max largest clusters
        clusters = [clusters[cluster_max_args[i]] for i in np.arange(np.min([n_max, n_clusters]))]

    return clusters

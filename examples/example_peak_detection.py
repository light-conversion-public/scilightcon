from scilightcon.fitting import detect_peaks
from scilightcon.datasets import load_csv_data
import matplotlib.pyplot as plt
import numpy as np

fname = 'data_test_detect_peaks.csv'

data, header = load_csv_data(fname)

x = data[:,0]
y = data[:,1]

method = "above_average"
clusters = detect_peaks(x, y, method = method, n_max=2)

plt.figure()

plt.plot(x, y, '.-')

print('clusters', clusters)
plt.plot(x, y, color='C0', alpha=0.3)
plt.xlim([x[0], x[-1]])

for cluster in clusters:
    plt.fill_between(x[cluster[0]:(cluster[1]+2)], np.min(y), np.max(y), facecolor = 'C2', alpha = 0.3)

plt.ylim([min([0.0, min(y)]), max(y)])

plt.xlabel("x")
plt.ylabel("y")
plt.grid()

plt.savefig('./doc/docs/img/detect_peaks_graph.png')
plt.show()

from scilightcon.datasets import load_csv_data
from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections
from scilightcon.utils import interpolate_and_multiply
import matplotlib.pyplot as plt
import numpy as np
import csv



D1, header = load_csv_data('White_LED_spectrum.csv')
x1 = D1[:,0]
y1 = D1[:,1]
D1 = (x1, y1)
# x1 = np.arange(0.0, 1000.0, 25.0)
# y1 = np.exp( - (x1 - 300.0) ** 2 / 20000)
# x2 = np.arange(200.0, 1000.0, 50.0)
# y2 = np.exp( - (x2 - 600.0) ** 2 / 10000)

D2, headers = load_EKSMA_OPTICS_mirror_reflections('Au')
x2 = D2[:,0]
y2 = D2[:,1]
D2 = (x2, y2)

D3 = interpolate_and_multiply(D1, D2)

fig = plt.figure('MSD-815')
plt.clf()

plt.plot(D1[0], D1[1]/np.max(D1[1]), label = 'White LED spectrum (D1)')
plt.plot(D2[0], D2[1]/np.max(D2[1]), label = 'Au mirror reflection (D2) ')
plt.plot(D3[0], D3[1]/np.max(D3[1]), label=r"D1$\cdot$D2")


plt.xlabel(header[0])
plt.ylabel(header[1])
plt.xlim(200, 1250)
plt.legend()
plt.grid()
plt.savefig('interpolate_and_multiply_plot.png')
plt.show()
print(D3)
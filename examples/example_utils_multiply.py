from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections
from scilightcon.utils import interpolate_and_multiply
import matplotlib.pyplot as plt
import numpy as np

# D1, _ = load_EKSMA_OPTICS_mirror_reflections('Al')
x1 = np.arange(0.0, 1000.0, 25.0)
y1 = np.exp( - (x1 - 300.0) ** 2 / 20000)
D1 = np.transpose([x1, y1])


x2 = np.arange(200.0, 1000.0, 50.0)
y2 = np.exp( - (x2 - 600.0) ** 2 / 10000)
D2 = np.transpose([x2, y2])

D3 = interpolate_and_multiply(D1, D2)

plt.figure('MSD-815')
plt.clf()

plt.scatter(D1[:,0], D1[:,1]/np.max(D1[:,1]), label = 'D1')
plt.scatter(D2[:,0], D2[:,1]/np.max(D2[:,1]), label = 'D2')
plt.scatter(D3[:,0], D3[:,1]/np.max(D3[:,1]), label=r"D1$\cdot$D2")

plt.legend()
plt.show()

print(D3)
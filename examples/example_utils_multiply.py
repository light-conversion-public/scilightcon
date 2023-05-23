from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections
import matplotlib.pyplot as plt
import numpy as np

D1, _ = load_EKSMA_OPTICS_mirror_reflections('Al')
x2 = np.arange(500.0, 1000.0, 1.0)
y2 = np.exp( - (x2 - 750.0) ** 2 / 5000) * np.max(D1[:,1])
D2 = [x2, y2]

plt.figure('MSD-815')
plt.clf()

plt.scatter(D1[:,0], D1[:,1], label = 'D1')
plt.scatter(D2[0], D2[1], label = 'D2')

plt.legend()
plt.show()
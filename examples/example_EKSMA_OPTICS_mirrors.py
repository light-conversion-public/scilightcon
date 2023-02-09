from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections
import matplotlib.pyplot as plt

plt.figure('reflectance')
plt.clf()

for material in ['Au', 'Ag', 'Al']:
    data, headers = load_EKSMA_OPTICS_mirror_reflections(material)

    plt.plot(data[:,0], data[:,1], label = material)

plt.xlabel(headers[0])
plt.ylabel(headers[1])
plt.legend()
plt.grid()

plt.show()
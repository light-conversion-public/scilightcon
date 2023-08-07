from scilightcon.datasets import load_EO_filter_transmissions
import matplotlib.pyplot as plt

plt.figure('reflectance')
plt.clf()

for material in ["lp_400nm", "lp_600nm", "sp_400nm", 'sp_600nm']:
    data, headers = load_EO_filter_transmissions(material)

    plt.plot(data[:,0], data[:,1], label = material)

plt.xlabel(headers[0])
plt.ylabel(headers[1])
plt.legend()
plt.grid()
plt.savefig('load_EO_filter_transmission.png')
plt.show()
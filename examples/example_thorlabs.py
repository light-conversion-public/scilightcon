from scilightcon.datasets import load_THORLABS_filter_transmissions
import matplotlib.pyplot as plt

plt.figure('reflectance')
plt.clf()

for material in ["DMLP425", "DMLP550", "FES0500", 'FES0800', "FGUV11"]:
    data, headers = load_THORLABS_filter_transmissions(material)

    plt.plot(data[:,0], data[:,1], label = material)

plt.xlabel(headers[0])
plt.ylabel(headers[1])
plt.legend()
plt.grid()
plt.savefig('load_thorlabs_transmission.png')
plt.show()
import sys
from scilightcon.datasets import load_atmospheric_data
import matplotlib.pyplot as plt

data, headers = load_atmospheric_data()
data_file_name = 'atmosphere.csv'


if 'pytest' not in sys.modules:
    plt.figure('reflectance')
    plt.clf()

    plt.plot(data[:,0], data[:,1])

    plt.xlabel(headers[0])
    plt.ylabel(headers[1])
    plt.grid()
    plt.savefig('load_atmospheric_data.png')
    plt.show()
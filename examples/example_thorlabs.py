from scilightcon.datasets import load_THORLABS_filter_transmissions
import matplotlib.pyplot as plt
import numpy as np

plt.figure('reflectance')
plt.clf()

for material in ["DMLP425", "DMLP550", "FES0500", 'FES0800', "FGUV11"]:
    data, headers = load_THORLABS_filter_transmissions(material)

    x_values = data[:,0]
    y_values = data[:,1]
    filtered_x = [x_values[0]]
    filtered_y = [y_values[0]]
    h = [1/3, 1/3, 1/3]
    for x, y in zip(x_values, y_values):
        if not filtered_x or x>= filtered_x[-1]:
            filtered_x.append(x)
            filtered_y.append(y)
        else:
            pass

    y_values_smooth = np.convolve(filtered_y, h, 'same')
    y_values_smooth[-1] = (filtered_y[-1] + filtered_y[-2])/2
    y_values_smooth[-2] = (filtered_y[-1] + filtered_y[-2])/2
    y_values_smooth[0] = (y_values[0] + y_values[1])/2  
    y_values_smooth[1] = (y_values[0] + y_values[1])/2
    plt.plot(filtered_x, y_values_smooth, label = material)

plt.xlabel(headers[0])
plt.ylabel(headers[1])
plt.legend()
plt.grid()
plt.savefig('load_thorlabs_transmission.png')
plt.show()
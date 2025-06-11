from scipy.io import loadmat
import numpy as np

data = loadmat('PMT QE.fig', squeeze_me=True, struct_as_record=False)

for child in data['hgS_070000'].children[0].children:
    if child.type == 'graph2d.lineseries':
        name = child.properties.DisplayName
        xdata = child.properties.XData
        ydata = child.properties.YData
        print(f"Found curve '{name}', data len: {len(xdata)}")
        np.savetxt(f"QE_Hamamatsu_{name}.csv",
        np.transpose([xdata, ydata]),
        header="Wavelength  (nm), QE (%)",
        fmt="%.6f",
        delimiter=', ')


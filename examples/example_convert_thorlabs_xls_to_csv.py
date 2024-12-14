from scilightcon.datasets import thorlabs_xls_to_csv
import matplotlib.pyplot as plt
import os

plt.figure()
# Note: you will need an XLS file from the Thorlabs website
wavl, trans = thorlabs_xls_to_csv('DMLP505.xls')
plt.plot(wavl, trans)
plt.xlabel('Wavelength')
plt.ylabel('Transmission')
plt.legend()
plt.grid('on')


if os.getenv("AZURE_EXTENSION_DIR") is not None:
    plt.savefig('./doc/docs/img/thorlabs_xls_to_csv.png')
else:
    plt.savefig('thorlabs_xls_to_csv.png')

plt.show()

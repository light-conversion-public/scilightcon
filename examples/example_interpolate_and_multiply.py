from scilightcon.datasets import load_csv_data
from scilightcon.datasets import load_EKSMA_OPTICS_mirror_reflections
from scilightcon.utils import interpolate_and_multiply
import matplotlib.pyplot as plt
import numpy as np

led_data, header = load_csv_data('White_LED_spectrum.csv')
led_x = led_data[:,0]
led_y = led_data[:,1]

mirror_data, headers = load_EKSMA_OPTICS_mirror_reflections('Au')
mirror_x = mirror_data[:,0]
mirror_y = mirror_data[:,1]

reflected_data = interpolate_and_multiply((led_x, led_y), (mirror_x, mirror_y))
reflected_x = reflected_data[0]
reflected_y = reflected_data[1]

plt.figure()

plt.plot(led_x, led_y/np.max(led_y), label = 'White LED spectrum before mirror')
plt.plot(mirror_x, mirror_y/np.max(mirror_y), label = 'Au mirror reflection')
plt.plot(reflected_x, reflected_y/np.max(reflected_y), label="White LED spectrum after mirror")

plt.xlabel(header[0])
plt.ylabel(header[1])
plt.xlim(200, 1000)
plt.ylim(0, None)
plt.legend()
plt.grid()

# plt.savefig('./doc/docs/img/example_interpolate_and_multiply.png')

plt.show()
import scilightcon
from scilightcon.utils._fixes import _open_binary
from scilightcon.fitting import fit_beam_profile_2d
import numpy as np
import pickle
import matplotlib.pyplot as plt

filepath =  _open_binary(scilightcon.datasets.DATA_MODULE, 'test_beam_profile.pkl')
matrix = pickle.load(filepath)['matrix']

result = fit_beam_profile_2d (matrix, method = 'gauss', options = {'decimation' : 2})

plt.figure()
plt.imshow(matrix, cmap='viridis', origin='lower')
plt.clim([0, None])
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gaussian beam profile fit')

metrics = ['mean_x', 'mean_y', 'phi', 'sigma_x', 'sigma_y', 'sigma_xy', 'sigma_p', 'sigma_s', 'ellipticity']

plt.text(0, np.shape(matrix)[0], '\n'.join([f'{metric} = {result[metric]:.3f}' for metric in metrics]), fontdict={'color': 'white'}, va='top')
plt.plot(result['mean_x'], result['mean_y'], '.k')
plt.plot([result['mean_x'] - result['sigma_p'] * np.cos(result['phi']), result['mean_x'] + result['sigma_p'] * np.cos(result['phi'])],
    [result['mean_y'] - result['sigma_p'] * np.sin(result['phi']), result['mean_y'] + result['sigma_p'] * np.sin(result['phi'])],
    '-k')

plt.plot([result['mean_x'] - result['sigma_s'] * np.cos(result['phi']+np.pi/2.0), result['mean_x'] + result['sigma_s'] * np.cos(result['phi']+np.pi/2.0)],
    [result['mean_y'] - result['sigma_s'] * np.sin(result['phi']+np.pi/2.0), result['mean_y'] + result['sigma_s'] * np.sin(result['phi']+np.pi/2.0)],
    '-k')

plt.savefig('./doc/docs/img/example_beam_profiler.png')
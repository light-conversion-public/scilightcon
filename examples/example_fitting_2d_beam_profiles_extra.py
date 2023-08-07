import numpy as np
from importlib import resources
import pickle
import scilightcon
from scilightcon.utils._fixes import _open_binary
from scilightcon.fitting import fit_beam_profile_2d
import matplotlib.pyplot as plt
import time

def test_beam_profiler_performance():
    sizes = [100, 200, 300, 350, 400]
    methods = ['iso', 'gauss']
    results = {method: [None] * len(sizes) for method in methods}

    for isize, size in enumerate(sizes):
        matrix = scilightcon.fitting._fitting_2d_beam_profiles._gauss2d_sigma_phi(
            np.arange(0, size), 
            np.arange(0, size), 
            A = 1.0, 
            xc = 150.0 / 400.0 * size, 
            yc = 250 / 400.0 * size, 
            sigma_p = 75.0 / 400.0 * size , 
            sigma_s = 25.0 / 400.0 * size ,       
            phi = 45.0 / 180.0 * np.pi, 
            y0 = 0.0)
        
        for method in methods:
            start_time = time.time()
            results[method][isize] = fit_beam_profile_2d (matrix, method = method, options = {'decimation' : 1})
            results[method][isize]['time'] = (time.time() - start_time)

    plt.figure('time')
    plt.clf()
    for method in methods:
        plt.semilogy(sizes, [item['time'] for item in results[method]], label = method)

    plt.legend()
    plt.grid()
    plt.show()


def test_fitting_beam_profiler_different_decimation():
    filepath =  _open_binary(scilightcon.datasets.DATA_MODULE, 'test_beam_profile.pkl')
    matrix = pickle.load(filepath)['matrix']

    # matrix = scilightcon.fitting._fitting_2d_beam_profiles._gauss2d_sigma_phi(
    #     np.arange(0, 400), 
    #     np.arange(0, 400), 
    #     A = 1.0, 
    #     xc = 200, 
    #     yc = 250, 
    #     sigma_p = 75.0, 
    #     sigma_s = 25.0,       
    #     phi = 30.0 / 180.0 * np.pi, 
    #     y0 = 0.0)
    
    plt.figure('profile')
    plt.imshow(matrix, cmap='viridis', origin='lower')
    plt.clim([0, None])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gaussian beam profile fit')

    decimations = [1, 2, 3, 4, 5, 6, 7, 8]
    #decimations = [1, 2]
    methods = ['iso', 'gauss']

    results = {method: [None] * len(decimations) for method in methods}
    
    for id, decimation in enumerate(decimations):
        for method in methods:
            start_time = time.time()
            results[method][id] = fit_beam_profile_2d (matrix, method = method, options = {'decimation' : decimation})
            results[method][id]['time'] = (time.time() - start_time)

    metrics = ['mean_x', 'mean_y', 'phi', 'sigma_x', 'sigma_y', 'sigma_xy', 'sigma_p', 'sigma_s', 'ellipticity']
    gauss_metric = 'gauss'
    plt.text(0, np.shape(matrix)[0], '\n'.join([f'{metric} = {results[gauss_metric][0][metric]:.3f}' for metric in metrics]), fontdict={'color': 'white'}, va='top')
    result = results[gauss_metric][0]
    plt.plot(result['mean_x'], result['mean_y'], '.k')
    plt.plot([result['mean_x'] - result['sigma_p'] * np.cos(result['phi']), result['mean_x'] + result['sigma_p'] * np.cos(result['phi'])],
             [result['mean_y'] - result['sigma_p'] * np.sin(result['phi']), result['mean_y'] + result['sigma_p'] * np.sin(result['phi'])],
             '-k')
    
    plt.plot([result['mean_x'] - result['sigma_s'] * np.cos(result['phi']+np.pi/2.0), result['mean_x'] + result['sigma_s'] * np.cos(result['phi']+np.pi/2.0)],
             [result['mean_y'] - result['sigma_s'] * np.sin(result['phi']+np.pi/2.0), result['mean_y'] + result['sigma_s'] * np.sin(result['phi']+np.pi/2.0)],
             '-k')


    plt.savefig('2d_beam_profile_gaussian_fit.png')

    plt.figure('compare')
    plt.clf()

    multipliactors = [1.0, 1.0, 180.0 / np.pi, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    for i,metric in enumerate(metrics):
        plt.subplot(3,3,i+1)
        for method in methods:
            plt.plot(decimations, [item[metric] * multipliactors[i] for item in results[method]], label = method)
            plt.xlabel('Decimation')
            plt.ylabel(metric)

        plt.legend()
        plt.grid()
    plt.show()


    
    return results

test_fitting_beam_profiler_different_decimation()
#test_beam_profiler_performance()
import numpy as np
from scipy.optimize import minimize

def fit_beam_profile_2d (matrix, method, options = {'decimation' : 1})-> dict:
    """ 
    Fitting of two-dimensional beam profiles using the Gaussian or ISO method.

    Examples:
        >>> import scilightcon
        >>> from scilightcon.utils._fixes import _open_binary
        >>> from scilightcon.fitting import fit_beam_profile_2d
        >>> import pickle
        >>> filepath = _open_binary(scilightcon.datasets.DATA_MODULE, 'test_beam_profile.pkl')
        >>> matrix = pickle.load(filepath)['matrix']
        >>> method = 'gauss'


    Args:
        matrix (array): matrix
        method (str): `iso` for ISO, `gauss` for Gaussian
        options (dict): Additional options (decimation)

    Returns:
        mean_x (float): position of the beam center in x axis
        mean_y (float): position of the beam center in y axis
        sigma_x (float): variance of beam along x axis
        sigma_y (float): variance of beam along y axis
        sigma_xy (float): standard deviation of x-y beam product
        sigma_p (float): variance of beam along its primary axis
        sigma_s (float): variance of beam along its secondary axis
        phi (float): beam angle (principal axis)
    """
    decimation = options.get('decimation') or 1
    matrix = matrix[::decimation, ::decimation]
    output = None

    init = _iterative_iso(matrix)

    if init['sigma_p'] < init['sigma_s']:
        temp = init['sigma_p']
        init['sigma_p'] = init['sigma_s']
        init['sigma_s'] = temp
        init['phi'] = init['phi'] + np.pi / 2

    if method =='iso':
        output = init

    if method == 'gauss':
        y0 = np.min(matrix)
        init_gauss = [
            np.max(matrix) - y0, # A
            init['mean_x'], # xc
            init['mean_y'], # yc
            (np.cos(init['phi']) / init['sigma_p']) ** 2.0 / 2.0 + (np.sin(init['phi']) / init['sigma_s']) ** 2.0 / 2.0, # a
            np.sin(2.0 * init['phi']) / 4.0 * (1.0 / init['sigma_p'] ** 2.0 - 1.0 / init['sigma_s'] ** 2.0), # b
            (np.sin(init['phi']) / init['sigma_p']) ** 2.0 / 2.0 + (np.cos(init['phi']) / init['sigma_s']) ** 2.0 / 2.0, # c
            y0  # y0
            ]
        output = _fit_gauss2d(matrix, init_gauss)    

        if output['sigma_p'] < output['sigma_s']:
            temp = output['sigma_p']
            output['sigma_p'] = output['sigma_s']
            output['sigma_s'] = temp

            output['phi'] = output['phi'] + np.pi / 2

    

    if output is None:
        raise ValueError(f"Invalid method {method}. Choose from: iso, gauss")

    output['ellipticity'] = output['sigma_s'] / output['sigma_p']

    multiplications = {'mean_x': decimation, 
                       'mean_y': decimation, 
                       'sigma_x': decimation, 
                       'sigma_y': decimation, 
                       'sigma_xy': decimation ** 2, 
                       'sigma_p': decimation, 
                       'sigma_s': decimation, 
                       'phi': 1.0,
                       'ellipticity': 1.0}
    output_dedecimated = {key : output[key] * multiplications[key] for key in output}
    return output_dedecimated


def _general_iso (matrix, mask = None):    
    xx, yy = np.meshgrid(np.arange(0, np.shape(matrix)[1]), np.arange(0, np.shape(matrix)[0]))

    if mask is not None:
        matrix = matrix * mask    
    sum_xy = np.sum(matrix)
    mean_x = np.sum(matrix * xx) / sum_xy
    mean_y = np.sum(matrix * yy) / sum_xy
    sigma_x = np.sqrt(np.sum(matrix * (xx - mean_x) ** 2) / sum_xy)
    sigma_y = np.sqrt(np.sum(matrix * (yy - mean_y) ** 2) / sum_xy)
    sigma_xy = np.sum(matrix * (xx - mean_x) * (yy - mean_y)) / sum_xy
    phi = 0.5 * np.arctan(2.0 * sigma_xy / (sigma_x ** 2 - sigma_y **2))
    gamma =  np.sign(sigma_x ** 2 - sigma_y ** 2)
    dx = 2.0 * np.sqrt(2.0) * np.sqrt((sigma_x ** 2 + sigma_y ** 2) + gamma * np.sqrt((sigma_x ** 2 - sigma_y ** 2) ** 2 + 4.0 * sigma_xy ** 2))
    dy = 2.0 * np.sqrt(2.0) * np.sqrt((sigma_x ** 2 + sigma_y ** 2) - gamma * np.sqrt((sigma_x ** 2 - sigma_y ** 2) ** 2 + 4.0 * sigma_xy ** 2))
    return {'mean_x': mean_x, 'mean_y':  mean_y, 'sigma_x' : sigma_x, 'sigma_y' : sigma_y, 'sigma_xy': sigma_xy, 'sigma_p' : dx / 4.0, 'sigma_s': dy / 4.0, 'phi': phi}

def _get_illuminated_pixels_mask(matrix):
    percentage = 0.05
    eta_T = 2.0
    width = int(np.shape(matrix)[1] * percentage)
    height = int (np.shape(matrix)[0] * percentage)
    area = [width if width > 0 else 1, height if height > 0 else 1] 
    averages = [np.average(matrix[0:area[0],0:area[1]]),    #upper left corner
                np.average(matrix[0:area[0],-area[1]:]),    #upper right corner
                np.average(matrix[-area[0]:,0:area[1]]),    #lower left corner
                np.average(matrix[-area[0]:,-area[1]:])     #lower right corner
                ]
    background_level = np.min(averages)
    noise_offset = np.min(averages) * eta_T
    percentile = np.percentile(matrix, 95)
    if (noise_offset  > percentile):        
        noise_offset = percentile
        print ('updated eta_T', percentile / np.min(averages))
    res = np.select([matrix>=noise_offset], [1])    
    return (res, background_level)

def _iterative_iso (matrix):
    xx, yy = np.meshgrid(np.arange(0, np.shape(matrix)[1]), np.arange(0, np.shape(matrix)[0]))
    illuminated_pixels, background_level = _get_illuminated_pixels_mask(matrix)    
    distance_coeff = 3.0
    matrix = matrix - background_level
    matrix = matrix * illuminated_pixels
    out = _general_iso (matrix)
    while True:
        out_old = out
        mask = np.logical_and(np.logical_and(xx > out['mean_x'] - distance_coeff * out['sigma_x'], xx < out['mean_x'] + distance_coeff * out['sigma_x']), 
                              np.logical_and(yy > out['mean_y'] - distance_coeff * out['sigma_y'], yy < out['mean_y'] + distance_coeff * out['sigma_y'])) + 0
        out = _general_iso (matrix, mask)                      
        if (out_old == out):
            break
    return out  

def _gauss2d_par(par, matrix):
    # Y = _gauss2d(np.arange(0, np.shape(matrix)[1]), np.arange(0, np.shape(matrix)[0]), par[0], par[1], par[2], par[3], par[4], par[5], par[6])                
    Y = _gauss2d(
        xaxis = np.arange(0, np.shape(matrix)[1]), 
        yaxis = np.arange(0, np.shape(matrix)[0]), 
        A = par[0], 
        xc = par[1], 
        yc = par[2],
        a = par[3], 
        b = par[4], 
        c = par[5], 
        y0 = par[6])                
    return Y

def _fun(par, args):
    matrix = args['matrix']
    score =  np.sum((matrix - _gauss2d_par(par, matrix)) ** 2)
    return score


def _gauss2d_sigma_phi(xaxis, yaxis, A, xc, yc, sigma_p, sigma_s, phi, y0):
    a = (np.cos(phi) / sigma_p) ** 2 / 2.0 + (np.sin(phi) / sigma_s) ** 2 / 2.0
    b = np.sin(2.0 * phi) / 4.0  * (1.0/ sigma_p ** 2 - 1.0 / sigma_s ** 2)
    c = (np.sin(phi) / sigma_p) ** 2 / 2.0 + (np.cos(phi) / sigma_s) ** 2 / 2.0

    return _gauss2d(xaxis, yaxis, A, xc, yc, a, b, c, y0)     

def _gauss2d(xaxis, yaxis, A, xc, yc, a, b, c, y0):
    xx, yy = np.meshgrid(xaxis, yaxis)
    result =  A * np.exp(- (a * (xx - xc) ** 2 + 2 * b * (xx - xc)*(yy - yc) + c * (yy - yc) ** 2)) + y0
    result[result>A] = A
    return result     

def _fit_gauss2d(matrix, init):
    out_minimize = minimize(_fun, init, method = 'Nelder-Mead', options = {'maxiter': len(matrix) * 10, 'maxfev': len(matrix) * 5, 'fatol': 1.0e-8}, args = {'matrix': matrix})    
    
    mean_x = out_minimize.x[1]
    mean_y = out_minimize.x[2]

    a = out_minimize.x[3]
    b = out_minimize.x[4]
    c = out_minimize.x[5]

    phi = 0.5 * np.arctan(2.0 * b / (a - c))

    # sigma_x = np.sqrt(np.cos(2.0 * phi) / (a * np.cos(phi) * np.cos(phi) - c * np.sin(phi) * np.sin(phi)))
    # sigma_y = np.sqrt(np.cos(2.0 * phi) / (-a * np.sin(phi) * np.sin(phi) + c * np.cos(phi) * np.cos(phi)))

    sigma_x = np.sqrt(1.0 / 2.0 / a)
    sigma_y = np.sqrt(1.0 / 2.0 / c)

    sigma_xy = b / (b * b - a * c) / 2.0

    sigma_p = (a + c + (a - c) / np.cos(2.0 * phi)) ** (-0.5)
    sigma_s = (2 * (a + c) - 1.0 / sigma_p / sigma_p) ** (-0.5)
    
    out_gauss = {'mean_x': mean_x, 'mean_y': mean_y, 'sigma_x': sigma_x, 'sigma_y': sigma_y, 'sigma_xy': sigma_xy,
                 'sigma_p': sigma_p, 'sigma_s': sigma_s, 'phi': phi}
    return out_gauss
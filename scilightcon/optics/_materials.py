from typing import List
import numpy as np
from typing import List, Tuple
from scipy.interpolate import interp1d
import math

class Material:
    _info = {}
    """
       Stores all the info on the chosen material                
    """
    def __init__ (self, info):
        self._info = info

    def get_refractive_index (self, wl: float, ray = 'both') -> List[float]:
       """  
        Returns array of calculated refractive index for a givern wavelength and target ray.
        First, the program takes the formula number and checks if the given wavelength is within the valid range.
        If the formula number is 0, it interpolates the datasets DataNWl and DataN to calculate the refractive index.
        If the formula number is in the range of 1-10, it calculates the refractive index using Sellmeier coefficients and corresponding equations.            
       """
       indices_dict = {'o': [0], 'e': [1], 'both': [0,1]}
       indices = indices_dict[ray]
       refractive_index_list = []
       for parameter_index in indices:

            if len(indices) == 1 and parameter_index >= len(self._info["Parameters"]):
                raise ValueError(f"Refractive index can not be calculated for {'ordinary' if 0 == parameter_index else 'extraordinary'} type of ray ")
                                   
            if parameter_index >= len(self._info["Parameters"]):
                 refractive_index_list.append(None)
                 continue
            
            formula = self._info["Parameters"][parameter_index]["Formula"]
            wl_range = self._info["Parameters"][parameter_index]["WlNRange"]
            if wl<wl_range[0] or wl>wl_range[1]:
                raise ValueError(f"For {'ordinary' if 0 == parameter_index else 'extraordinary'} type of ray " +
                                 f"the wavelenght should be in range between {wl_range[0]} and {wl_range[1]}")
                
            if formula == 0:
                n = _get_refractive_index_from_raw_data(
                    wl,
                    self._info["Parameters"][parameter_index]["DataNWl"], 
                    self._info["Parameters"][parameter_index]["DataN"])
                refractive_index_list.append(n)
            else:           
                if formula > 0 and formula < 10: 
                    sellmeier_coeffs = self._info["Parameters"][parameter_index]["SellmeierCoeffs"]
                elif formula == 10:
                    if parameter_index ==0: 
                        sellmeier_coeffs = self._info["Parameters"][parameter_index]["XC"]
                    else: 
                        sellmeier_coeffs = self._info["Parameters"][parameter_index]["YC"]

                refractive_index_list.append(_get_refractive_index_from_sellmeier_coeffs(wl, formula, sellmeier_coeffs))
            
       return refractive_index_list


def _get_refractive_index_from_sellmeier_coeffs(wl: float, formula_index: int, sellmeier_coeffs: List[float]) -> float:
    n_coeffs = len(sellmeier_coeffs)
    if n_coeffs ==0: return ([None]*len(wl))
    C = np.append(sellmeier_coeffs, [0]*(17-len(sellmeier_coeffs)))
    
    # formula 1 
    if formula_index==1:
        return np.sqrt(1+C[0]+C[1]/(1-(C[2]/wl)**2)+C[3]/(1-(C[4]/wl)**2)+C[5]/(1-(C[6]/wl)**2)+C[7]/(1-(C[8]/wl)**2)+C[9]/(1-(C[10]/wl)**2)+C[11]/(1-(C[12]/wl)**2)+C[13]/(1-(C[14]/wl)**2)+C[15]/(1-(C[16]/wl)**2))
    # formula 2 
    if formula_index==2:
        return np.sqrt(1+C[0]+C[1]/(1-C[2]/(wl)**2)+C[3]/(1-C[4]/(wl)**2)+C[5]/(1-C[6]/(wl)**2)+C[7]/(1-C[8]/(wl)**2)+C[9]/(1-C[10]/(wl)**2)+C[11]/(1-C[12]/(wl)**2)+C[13]/(1-C[14]/(wl)**2)+C[15]/(1-C[16]/(wl)**2))
    # formula 3
    if formula_index==3:
        return np.sqrt(C[0]+C[1]*(wl)**C[2]+C[3]*(wl)**C[4]+C[5]*(wl)**C[6]+C[7]*(wl)**C[8]+C[9]*(wl)**C[10]+C[11]*(wl)**C[12]+C[13]*(wl)**C[14]+C[15]*(wl)**C[16])
    # formula 4 
    if formula_index==4:
        return np.sqrt(C[0]+C[1]*(wl)**C[2]/((wl)**2-(C[3])**C[4])+C[5]*(wl)**C[6]/((wl)**2-(C[7])**C[8])+C[9]*(wl)**C[10]+C[11]*(wl)**C[12]+C[13]*(wl)**C[14]+C[15]*(wl)**C[16])
    # formula 5
    if formula_index==5:
        return C[0]+C[1]*(wl)**C[2]+C[3]*(wl)**C[4]+C[5]*(wl)**C[6]+C[7]*(wl)**C[8]+C[9]*(wl)**C[10]
    # formula 6 
    if formula_index==6:
        return 1+C[0]+C[1]/(C[2]-(wl)**-2)+C[3]/(C[4]-(wl)**-2)+C[5]/(C[6]-(wl)**-2)+C[7]/(C[8]-(wl)**-2)+C[9]/(C[10]-(wl)**-2)
    # formula 7
    if formula_index==7:
        return C[0]+C[1]/((wl)**2-0.028)+C[2]/(wl**2-0.028)**2+C[3]*(wl)**2+C[4]*(wl)**4+C[5]*(wl)**6
    # formula 8
    if formula_index==8:
        tmp = C[0]+C[1]*(wl)**2/((wl)**2-C[2])+C[3]*(wl)**2
        return np.sqrt((2*tmp+1)/(1-tmp))
    # formula 9 
    if formula_index==9:
        return np.sqrt(C[0]+C[1]/((wl)**2-C[2])+C[3]*(wl-C[4])/((wl-C[4])**2+C[5]))
    # formula 10   
    if formula_index==10:
        return np.sqrt( C[0] + C[1] / ((wl ** 2) - C[2]) + (C[3] * (wl ** 2)) / ((wl ** 2) * C[4] - 1) + C[5] / ((wl ** 4) - C[6]) + (C[7] * (wl ** 2)) / (C[8] * (wl ** 4) - 1) + (C[9] * (wl ** 4)) / (C[10] * (wl ** 4) - 1)); 

def load_material(name: str) -> Material:
   from ..datasets import _materials
   
   name = name.lower()
   
   for key in _materials:
      if _materials[key]["Name"].lower() == name or _materials[key]["Chemformula"].lower() == name or name in [alias.lower() for alias in _materials[key]['Alias']]:
          return Material(_materials[key])
   raise ValueError("Material not found")

def _get_refractive_index_from_raw_data(x0: float, x: List[float], y: List[float]) -> float:
    '''This function interpolates x,y data and returns function's value at x0'''
    f2 = interp1d(x, y, kind = "linear") 
    return f2(x0)


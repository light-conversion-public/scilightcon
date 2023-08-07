from typing import List
import numpy as np
from typing import List, Tuple
from scipy.interpolate import interp1d
from scilightcon.utils import c
import math
from ._utils import _get_refractive_index_from_raw_data
from ._GVD_and_TOD_calculator import _get_refractive_index_second_derivative
from ._GVD_and_TOD_calculator import _get_refractive_index_third_derivative

class Material:
    """Class for storing and calculating optical properties (refractive index, GVD, TOD) of different materials.
    
    Examples:
        >>> from scilightcon.optics import load_material
        >>> zinc_oxide = load_material('Zinc oxide')
        >>> n_o, n_e = zinc_oxide.get_refractive_index(1.03, ray='both')
        >>> n_o
        1.9417466542383048
        >>> n_e
        1.9565995766753679
        >>> gvd = zinc_oxide.get_GVD(1.03, ray='o')
        >>> gvd
        array([283.0382719])
        >>> tod = zinc_oxide.get_TOD(1.03, ray='o')
        >>> tod
        array([264.18233337])
        
    """

    _info = {}
    def __init__ (self, info):
        self._info = info

    def get_GVD (self, wl: float, ray = 'o') -> List[float]:
        """  
        The function computes and returns the group velocity dispersion (GVD) for a specific material, considering the chosen wavelength and a type of ray.
        Examples:
            >>> from scilightcon.optics import load_material
            >>> zinc_oxide = load_material('Zinc oxide')
            >>> gvd = zinc_oxide.get_GVD(1.03, ray='o')
            >>> gvd
            array([283.0382719])
        
        Args:
            wl (float): Wavelength in micrometers   
            ray (str): `o` for ordinary, `e` for extraordinary

        Returns:
            An array of material's GVD       
        """
        
        indices_dict = {'o': [0], 'e': [1]}
        indices = indices_dict[ray]

        for parameter_index in indices:
            formula_index = self._info["Parameters"][parameter_index]["Formula"]
            if formula_index == 0:
                raise ValueError(f"GVD can not be calculated for material with formula index = 0")
            if len(indices) == 1 and parameter_index >= len(self._info["Parameters"]):
                raise ValueError(f"GVD index can not be calculated for {'ordinary' if 0 == parameter_index else 'extraordinary'} type of ray ")
            wl_range = self._info["Parameters"][parameter_index]["WlNRange"]
            if wl<wl_range[0] or wl>wl_range[1]:
                raise ValueError(f"For {'ordinary' if 0 == parameter_index else 'extraordinary'} type of ray " +
                                 f"the wavelenght should be in range between {wl_range[0]} and {wl_range[1]}")
            
            wl_t = self._info["Parameters"][parameter_index]["WlNRange"][1]
            data_n_wl = self._info["Parameters"][parameter_index]["DataNWl"]
            data_n =self._info["Parameters"][parameter_index]["DataN"]
            sellmeier_coeffs = self._info["Parameters"][parameter_index]["SellmeierCoeffs"]
            XC = self._info["Parameters"][parameter_index]["XC"]
            YC = self._info["Parameters"][parameter_index]["YC"]
            
        second_derivative =np.array(_get_refractive_index_second_derivative(wl, wl_t, formula_index, parameter_index, sellmeier_coeffs, data_n_wl, data_n, XC, YC))
        
        gvd = second_derivative * (wl**3 / (2.0 * math.pi * c * c))*10**-3
        return gvd

    def get_TOD (self, wl: float, ray = 'o') -> List[float]:
        """  
        The function computes and returns the third-order dispersion (TOD) for a specific material, considering the chosen wavelength and a type of ray.
        
        Examples:
            >>> from scilightcon.optics import load_material
            >>> zinc_oxide = load_material('Zinc oxide')
            >>> tod = zinc_oxide.get_TOD(1.03, ray='o')
        
        Args:
            wl (float): Wavelength in micrometers   
            ray (str): `o` for ordinary, `e` for extraordinary  
        
        Returns:
            An array of material's TOD       
        """
        indices_dict = {'o': [0], 'e': [1]}
        indices = indices_dict[ray]

        for parameter_index in indices:
            formula_index = self._info["Parameters"][parameter_index]["Formula"]
            if formula_index == 0:
                raise ValueError(f"TOD can not be calculated for material with formula index = 0")
            if len(indices) == 1 and parameter_index >= len(self._info["Parameters"]):
                raise ValueError(f"TOD index can not be calculated for {'ordinary' if 0 == parameter_index else 'extraordinary'} type of ray ")
            wl_range = self._info["Parameters"][parameter_index]["WlNRange"]
            if wl<wl_range[0] or wl>wl_range[1]:
                raise ValueError(f"For {'ordinary' if 0 == parameter_index else 'extraordinary'} type of ray " +
                                 f"the wavelenght should be in range between {wl_range[0]} and {wl_range[1]}")
            
            wl_b = self._info["Parameters"][parameter_index]["WlNRange"][0]
            wl_t = self._info["Parameters"][parameter_index]["WlNRange"][1]
            data_n_wl = self._info["Parameters"][parameter_index]["DataNWl"]
            data_n =self._info["Parameters"][parameter_index]["DataN"]
            sellmeier_coeffs = self._info["Parameters"][parameter_index]["SellmeierCoeffs"]
            XC = self._info["Parameters"][parameter_index]["XC"]
            YC = self._info["Parameters"][parameter_index]["YC"]
            
        third_derivative =np.array(_get_refractive_index_third_derivative(wl, wl_b, wl_t, formula_index, parameter_index, sellmeier_coeffs, data_n_wl, data_n, XC, YC))
        second_derivative =np.array(_get_refractive_index_second_derivative(wl, wl_t, formula_index, parameter_index, sellmeier_coeffs, data_n_wl, data_n, XC, YC))
        
        tod = (-wl**4 / (4 * math.pi * math.pi * c * c * c)) * (3* second_derivative + wl* third_derivative) * 1.0e-6 
        return tod

    def get_refractive_index (self, wl: float, ray = 'both') -> List[float]:
       """  
        The function computes and returns the refractive index of a specific material, considering the chosen wavelength and the type of ray.
    
        Examples:
            >>> from scilightcon.optics import load_material
            >>> zinc_oxide = load_material('Zinc oxide')
            >>> n_o, n_e = zinc_oxide.get_refractive_index(1.03, ray='both')
            >>> n_o
            1.9417466542383048
            >>> n_e
            1.9565995766753679

               
        Args:
            wl (float): Wavelength in micrometers   
            ray (str): `o` for ordinary, `e` for extraordinary, `both` for both ordinary and extraordinary rays respectively

        Returns:
            An array of material's refractive index or indexes if calculated for both types of rays       
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
    
    if formula_index==1:
        return np.sqrt(1+C[0]+C[1]/(1-(C[2]/wl)**2)+C[3]/(1-(C[4]/wl)**2)+C[5]/(1-(C[6]/wl)**2)+C[7]/(1-(C[8]/wl)**2)+C[9]/(1-(C[10]/wl)**2)+C[11]/(1-(C[12]/wl)**2)+C[13]/(1-(C[14]/wl)**2)+C[15]/(1-(C[16]/wl)**2))
    if formula_index==2:
        return np.sqrt(1+C[0]+C[1]/(1-C[2]/(wl)**2)+C[3]/(1-C[4]/(wl)**2)+C[5]/(1-C[6]/(wl)**2)+C[7]/(1-C[8]/(wl)**2)+C[9]/(1-C[10]/(wl)**2)+C[11]/(1-C[12]/(wl)**2)+C[13]/(1-C[14]/(wl)**2)+C[15]/(1-C[16]/(wl)**2))
    if formula_index==3:
        return np.sqrt(C[0]+C[1]*(wl)**C[2]+C[3]*(wl)**C[4]+C[5]*(wl)**C[6]+C[7]*(wl)**C[8]+C[9]*(wl)**C[10]+C[11]*(wl)**C[12]+C[13]*(wl)**C[14]+C[15]*(wl)**C[16])
    if formula_index==4:
        return np.sqrt(C[0]+C[1]*(wl)**C[2]/((wl)**2-(C[3])**C[4])+C[5]*(wl)**C[6]/((wl)**2-(C[7])**C[8])+C[9]*(wl)**C[10]+C[11]*(wl)**C[12]+C[13]*(wl)**C[14]+C[15]*(wl)**C[16])
    if formula_index==5:
        return C[0]+C[1]*(wl)**C[2]+C[3]*(wl)**C[4]+C[5]*(wl)**C[6]+C[7]*(wl)**C[8]+C[9]*(wl)**C[10]
    if formula_index==6:
        return 1+C[0]+C[1]/(C[2]-(wl)**-2)+C[3]/(C[4]-(wl)**-2)+C[5]/(C[6]-(wl)**-2)+C[7]/(C[8]-(wl)**-2)+C[9]/(C[10]-(wl)**-2)
    if formula_index==7:
        return C[0]+C[1]/((wl)**2-0.028)+C[2]/(wl**2-0.028)**2+C[3]*(wl)**2+C[4]*(wl)**4+C[5]*(wl)**6
    if formula_index==8:
        tmp = C[0]+C[1]*(wl)**2/((wl)**2-C[2])+C[3]*(wl)**2
        return np.sqrt((2*tmp+1)/(1-tmp))
    if formula_index==9:
        return np.sqrt(C[0]+C[1]/((wl)**2-C[2])+C[3]*(wl-C[4])/((wl-C[4])**2+C[5])) 
    if formula_index==10:
        return np.sqrt( C[0] + C[1] / ((wl ** 2) - C[2]) + (C[3] * (wl ** 2)) / ((wl ** 2) * C[4] - 1) + C[5] / ((wl ** 4) - C[6]) + (C[7] * (wl ** 2)) / (C[8] * (wl ** 4) - 1) + (C[9] * (wl ** 4)) / (C[10] * (wl ** 4) - 1)); 

def load_material(name: str) -> Material:
   """Loads material's data.
    Args:
        name (str): Material's name, chemformula or alias  
        
    Examples:
        >>> from scilightcon.optics import load_material
        >>> zinc_oxide = load_material('Zinc oxide')
        >>> n_o, n_e = zinc_oxide.get_refractive_index(1.03, ray = 'both')
        >>> n_o
        1.9417466542383048
        >>> n_e
        1.9565995766753679

    Returns:
        Material's object
   """
   from ..datasets import _materials
   
   name = name.lower()
   
   for key in _materials:
      if _materials[key]["Name"].lower() == name or _materials[key]["Chemformula"].lower() == name or name in [alias.lower() for alias in _materials[key]['Alias']]:
          return Material(_materials[key])
   raise ValueError("Material not found")
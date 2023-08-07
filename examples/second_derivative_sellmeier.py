import sympy as sp
from sympy import symbols
import numpy as np

wl, C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16 = symbols('wl, C[0], C[1], C[2], C[3], C[4], C[5], C[6], C[7], C[8], C[9], C[10], C[11], C[12], C[13], C[14], C[15], C[16]')

#     # formula 1 
#     eq1 = sp.sqrt(1+C0+C1/(1-(C2/wl)**2)+C3/(1-(C4/wl)**2)+C5/(1-(C6/wl)**2)+C7/(1-(C8/wl)**2)+C9/(1-(C10/wl)**2)+C11/(1-(C12/wl)**2)+C13/(1-(C14/wl)**2)+C15/(1-(C16/wl)**2))
    
#     # formula 2 
        #  eq2 = sp.sqrt(1+C0+C1/(1-C2/(wl)**2)+C3/(1-C4/(wl)**2)+C5/(1-C6/(wl)**2)+C7/(1-C8/(wl)**2)+C9/(1-C10/(wl)**2)+C11/(1-C12/(wl)**2)+C13/(1-C14/(wl)**2)+C15/(1-C16/(wl)**2))

#     # formula 3
#     if formula_index==3:
#         return np.sqrt(C[0]+C[1]*(wl)**C[2]+C[3]*(wl)**C[4]+C[5]*(wl)**C[6]+C[7]*(wl)**C[8]+C[9]*(wl)**C[10]+C[11]*(wl)**C[12]+C[13]*(wl)**C[14]+C[15]*(wl)**C[16])
#     eq3 = sp.sqrt(C0+C1*(wl)**C2+C3*(wl)**C4+C5*(wl)**C6+C7*(wl)**C8+C9*(wl)**C10+C11*(wl)**C12+C13*(wl)**C14+C15*(wl)**C16)
    
#     # formula 4 
#     if formula_index==4:
#         return np.sqrt(C[0]+C[1]*(wl)**C[2]/((wl)**2-(C[3])**C[4])+C[5]*(wl)**C[6]/((wl)**2-(C[7])**C[8])+C[9]*(wl)**C[10]+C[11]*(wl)**C[12]+C[13]*(wl)**C[14]+C[15]*(wl)**C[16])
    #  eq4 = sp.sqrt(C0+C1*(wl)**C2/((wl)**2-(C3)**C4)+C5*(wl)**C6/((wl)**2-(C7)**C8)+C9*(wl)**C10+C11*(wl)**C12+C13*(wl)**C14+C15*(wl)**C16)   
   
#     # formula 5
#     if formula_index==5:
#         return C[0]+C[1]*(wl)**C[2]+C[3]*(wl)**C[4]+C[5]*(wl)**C[6]+C[7]*(wl)**C[8]+C[9]*(wl)**C[10]
#     eq5 = C0+C1*(wl)**C2+C3*(wl)**C4+C5*(wl)**C6+C7*(wl)**C8+C9*(wl)**C10
    
#     # formula 6 
#     if formula_index==6:
#         return 1+C[0]+C[1]/(C[2]-(wl)**-2)+C[3]/(C[4]-(wl)**-2)+C[5]/(C[6]-(wl)**-2)+C[7]/(C[8]-(wl)**-2)+C[9]/(C[10]-(wl)**-2)
#     eq6 = 1+C0+C1/(C2-(wl)**-2)+C3/(C4-(wl)**-2)+C5/(C6-(wl)**-2)+C7/(C8-(wl)**-2)+C9/(C10-(wl)**-2)    
    
#     # formula 7
#     if formula_index==7:
#         return C[0]+C[1]/((wl)**2-0.028)+C[2]/(wl**2-0.028)**2+C[3]*(wl)**2+C[4]*(wl)**4+C[5]*(wl)**6
#     eq7 = C0+C1/((wl)**2-0.028)+C2/(wl**2-0.028)**2+C3*(wl)**2+C4*(wl)**4+C5*(wl)**6
   
#     # formula 8
#     if formula_index==8:
#         tmp = C[0]+C[1]*(wl)**2/((wl)**2-C[2])+C[3]*(wl)**2
#         return np.sqrt((2*tmp+1)/(1-tmp))
#     eq8 = sp.sqrt((2*(C0+C1*(wl)**2/((wl)**2-C2)+C3*(wl)**2)+1)/(1-(C0+C1*(wl)**2/((wl)**2-C2)+C3*(wl)**2)))
    
#     # formula 9 
#     if formula_index==9:
#         return np.sqrt(C[0]+C[1]/((wl)**2-C[2])+C[3]*(wl-C[4])/((wl-C[4])**2+C[5]))
#     eq9 = sp.sqrt(C0+C1/((wl)**2-C2)+C3*(wl-C4)/((wl-C4)**2+C5))     
    
#     # formula 10   
#     if formula_index==10:
#         return np.sqrt(C[0]+C[1]/((wl**2)-C[2])+(C[3]*(wl**2))/((wl**2)*C[4]-1)+C[5]/((wl**4)-C[6])+(C[7]*(wl**2))/(C[8]*(wl**4)-1)+(C[9]*(wl**4))/(C[10]*(wl**4)-1)) 
#     eq10 = sp.sqrt(C0+C1/((wl**2)-C2)+(C3*(wl**2))/((wl**2)*C4-1)+C5/((wl**4)-C6)+(C7*(wl**2))/(C8*(wl**4)-1)+(C9*(wl**4))/(C10*(wl**4)-1)) 


#derivative_eq = sp.diff(eq2, wl, wl)


    # if formula_index == 0:
        # raise ValueError(f"GVD can not be calculated for material with formula index = 0")
        # deltawl = 1.0e-5

        # if wl + 2.0 * deltawl >= wl_t:
        #     wl -= 2.0 * deltawl
  
        # n0 = _get_refractive_index_from_raw_data(
        #                 wl + deltawl,
        #                 data_n_wl, 
        #                 data_n)
        # n1 = _get_refractive_index_from_raw_data(
        #                 wl,
        #                 data_n_wl, 
        #                 data_n)
        # n2 = _get_refractive_index_from_raw_data(
        #                 wl + 2.0 * deltawl,
        #                 data_n_wl, 
        #                 data_n)    
        # n= ((n2 - 2.0 * n0 + n1) / deltawl**2.0 )
        # refractive_index_second_derivative_list.append(n)



        # delta_wl = 1.0e-2

            # if wl + 1.5 * delta_wl >= wl_t:
            #     wl -= 1.5 * delta_wl

            # if wl - 1.5 * delta_wl <= wl_b:
            #     wl += 1.5 * delta_wl

            # d2P = (
            #     _get_refractive_index_from_raw_data(wl + delta_wl, data_n_wl, data_n)
            #     - 2.0 * _get_refractive_index_from_raw_data(wl, data_n_wl, data_n)
            #     + _get_refractive_index_from_raw_data(wl - delta_wl, data_n_wl, data_n)) / delta_wl**2
            

            # d3P = (
            #     _get_refractive_index_from_raw_data(wl + 1.5 * delta_wl, data_n_wl, data_n)- 3.0
            #     * _get_refractive_index_from_raw_data(wl + 0.5 * delta_wl, data_n_wl, data_n)+ 3.0
            #     * _get_refractive_index_from_raw_data(wl - 0.5 * delta_wl, data_n_wl, data_n) - 
            #       _get_refractive_index_from_raw_data(wl - 1.5 * delta_wl, data_n_wl, data_n))/delta_wl**3
            
    
            # n = 3.0 * d2P + wl * d3P
            # refractive_index_third_derivative_list.append(n)
    
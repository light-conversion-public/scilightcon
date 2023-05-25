from typing import List

class Material:
    _info = {}

    def __init__ (self, info):
        self._info = info

    def get_refractive_index (self, wavelength: float, ray = 'both') -> List[float]:
        """
        Returns array of calculated refractive index for a givern wavelength and target ray. NEED UPDATE                
        """
        self._info

        raise NotImplementedError()



def load_material(key: str) -> Material:
    # reikia pereiti per scilightcon.datasets._materials duomenu bazer
    # radus reikiama medziaga grazinti atitinkama elementa (pvz scilightcon.datasets._materials['ZnO'])
    # ir ji panaudoti konstruktoriuje: return Material(scilightcon.datasets._materials['ZnO'])
    
    raise NotImplementedError()
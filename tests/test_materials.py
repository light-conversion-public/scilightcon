import scilightcon
import pytest

def test_materials():
    assert (len(scilightcon.datasets._materials) > 0)

def test_GVD():
    from scilightcon.optics import load_material
  
    # 1 - loads material and correct refractive index of ordinary and extraordinary beams
    zinc = load_material('Zinc oxide')
    gvd = zinc.get_GVD(1.03, ray='o')
    gvd = zinc.get_GVD(1.03, ray='e')

    with pytest.raises(ValueError):
        zinc.get_GVD(0.4)

    with pytest.raises(ValueError):
        zinc.get_GVD(4.6)
    
    # 2 - loads correct refractive index of ordinary beam
    ri = zinc.get_GVD(1.03, ray='o')
    assert (len(ri) == 1)
    assert (abs(ri[0] - 283.025) < 0.1)

    # TO DO WHEN OPTICS TOOLBOX WILL BE FIXED 
    # # 3 - loads correct refractive index of extraordinary beam
    # ri = zinc.get_GVD(1.03, ray='e')
    # assert (len(ri) == 1)
    # assert (abs(ri[0] - GVD for e beam) < 0.1)
     
 
    # 4 - anisotropic medium by alias
    fs = load_material('Pb')
    with pytest.raises(ValueError):
        fs.get_GVD(4.6)

def test_TOD():
    from scilightcon.optics import load_material
  
    # 1 - loads material and correct refractive index of ordinary and extraordinary beams
    zinc = load_material('Zinc oxide')
    gvd = zinc.get_TOD(1.03, ray='o')
    gvd = zinc.get_TOD(1.03, ray='e')

    with pytest.raises(ValueError):
        zinc.get_TOD(0.4)

    with pytest.raises(ValueError):
        zinc.get_TOD(4.6)
    
    # 2 - loads correct refractive index of ordinary beam
    ri = zinc.get_TOD(1.03, ray='o')
    assert (len(ri) == 1)
    assert (abs(ri[0] - 264.444) < 1)
    
    # TO DO WHEN OPTICS TOOLBOX WILL BE FIXED 
    # # 3 - loads correct refractive index of extraordinary beam
    # ri = zinc.get_GVD(1.03, ray='e')
    # assert (len(ri) == 1)
    # assert (abs(ri[0] - TOD for e beam) < 0.1)

    # 4 - anisotropic medium by alias
    fs = load_material('Pb')
    with pytest.raises(ValueError):
        fs.get_GVD(4.6)

def test_refractive_index():
    from scilightcon.optics import load_material

    # 1 - loads material
    zinc = load_material('Zinc oxide')
    assert (zinc is not None)

    # 2 - raises ValueError when material not found
    with pytest.raises(ValueError):
        load_material('Whatever')

    # 3 - loads correct refractive index of ordinary beam
    ri = zinc.get_refractive_index(1.03, ray='o')
    assert (len(ri) == 1)
    assert (abs(ri[0] - 1.941747) < 1.0e-5)
    
    # 4 - loads correct refractive index of extraordinary beam
    ri = zinc.get_refractive_index(1.03, ray='e')
    assert (len(ri) == 1)
    assert (abs(ri[0] - 1.956600) < 1.0e-5)

    # 5 - loads refractive indices of both beams
    ri = zinc.get_refractive_index(1.03, ray='both')
    assert (ri == zinc.get_refractive_index(1.03))
    assert (len(ri) == 2)
    assert (ri[0] == zinc.get_refractive_index(1.03, ray='o'))
    assert (ri[1] == zinc.get_refractive_index(1.03, ray='e'))

    with pytest.raises(ValueError):
        zinc.get_refractive_index(0.4)

    with pytest.raises(ValueError):
        zinc.get_refractive_index(4.1)

    # 6 - anisotropic medium by alias
    fs = load_material('Pb')
    assert (len(fs.get_refractive_index(1.03)) == 2)
    assert (fs.get_refractive_index(1.03)[1] == None)
    assert (len(fs.get_refractive_index(1.03, ray='o')) == 1)
    with pytest.raises(ValueError):
        fs.get_refractive_index(1.03, ray='e')
#! /usr/bin/python
#
# -updated for python3 (print) and updated for changes in python modules
#
#
# mixes pure fusion materials based on FESS-FNSF, ARIES, EUDEMO and other designs
# -can be used for mixing homogenized regions
#
# Improvements to make:
# -should use a function to create the constituent citation list for each mixture
#
# references for FNSF compositions
#
# MadaniUWFDM1423_2015 https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1423.pdf
# EliasUWFMD1424_2015 https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1424.pdf
# HarbFusSciTec_2017 https://doi.org/10.1080/15361055.2017.1333846.
# ElGuebalyFusSciTec_2017 https://doi.org/10.1080/15361055.2017.1333865
# DavisFusEngDes_2018 https://doi.org/10.1016/j.fusengdes.2017.06.008
# BohmFusSciTec_2019 https://doi.org/10.1080/15361055.2019.1600930
# SchnabelNDS_2024 preprint https://arxiv.org/pdf/2311.10063.pdf
#
import os
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary
#
# Load material library (created using pyne)

def load_matlib():
    mat_lib=MaterialLibrary()
    mat_lib.from_hdf5("PureFusionMaterials_libv1.h5", datapath='/materials') # don't set datapath,nucpath...will be pyne default values *** need to indicate datapath in new pyne now
    return mat_lib
   
# Mix Materials by Volume

"""
FNSFFW    (34% FS MF82H, 66% He)
"""
# fullreference DavisFusEngDes_2018 https://doi.org/10.1016/j.fusengdes.2017.06.008
def mix_FNSFFW(material_library):
    mix=MultiMaterial({material_library['MF82H']:0.34,material_library['HeT410P80']:0.66})
    FNSFFW_mat=mix.mix_by_volume()
    FNSFFW_mat.metadata['mat_number']=9
    FNSFFW_mat.metadata['mixturecitation']='DavisFusEngDes_2018'
    constituentCitationList=[str(material_library['MF82H'].metadata['citation']),str(material_library['HeT410P80'].metadata['citation'])]
    constituentCitation=" ".join(constituentCitationList)
    FNSFFW_mat.metadata['constituentcitation']=constituentCitation
    print('FNSFFW_mat  ', FNSFFW_mat.metadata['mat_number'], FNSFFW_mat.density)
    print("   Constituent Citations: ", constituentCitation)
    FNSFFW_mat=FNSFFW_mat.expand_elements()
    return FNSFFW_mat

"""
FNSFFWstruct    (100% FS MF82H)
"""
def mix_FNSFFWstruct(material_library):
    mix=MultiMaterial({material_library['MF82H']:1.00})
    FNSFFWstruct_mat=mix.mix_by_volume()
    FNSFFWstruct_mat.metadata['mat_number']=26
    FNSFFWstruct_mat.metadata['mixturecitation']='DavisFusEngDes_2018'
    print('FNSFFWstruct_mat  ', FNSFFWstruct_mat.metadata['mat_number'], FNSFFWstruct_mat.density)
    FNSFFWstruct_mat=FNSFFWstruct_mat.expand_elements()
    return FNSFFWstruct_mat

"""
response function material reIron (100% Iron)
"""
def mix_reIron(material_library):
    mix=MultiMaterial({material_library['Fe']:1.00})
    reIron_mat=mix.mix_by_volume()
    reIron_mat.metadata['mat_number']=312
    reIron_mat.metadata['mixturecitation']=str(material_library['Fe'].metadata['citation'])
    print('reIron_mat  ', reIron_mat.metadata['mat_number'], reIron_mat.density) 
    reIron_mat=reIron_mat.expand_elements()
    return reIron_mat
#
# blanket materials

#FNSF OB DCLL Blanket (73.7% LiPb (90% Li-6), 14.9% He/void, 7.5% FS, 3.9% SiC)
# fullreference EliasUWFMD1424_2015 https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1424.pdf
#FNSF IB DCLL Blanket (80% LiPb (90% Li-6), 12% He/void, 5% FS, 3% SiC)
# fullreference MadaniUWFDM1423_2015 https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1423.pdf

# FNSF DCLL approximate average    77%                  13.5%        6%  3.5%

"""
FNSFDCLL 77% LiPb (90% Li-6), 13.5% He/void, 6% FS, 3.5% SiC
"""
def mix_FNSFDCLL(material_library):
    mix=MultiMaterial({material_library['MF82H']:0.06, material_library['Pb157Li90']:0.77, material_library['HeT410P80']: 0.135, material_library['SiC']: 0.035})
    FNSFDCLL_mat=mix.mix_by_volume()
    FNSFDCLL_mat.metadata['mat_number']=220
    FNSFDCLL_mat.metadata['mixturecitation']='EliasUWFMD1424_2015 and MadaniUWFDM1423_2015'
    constituentCitationList=[str(material_library['MF82H'].metadata['citation']), str(material_library['Pb157Li90'].metadata['citation']), str(material_library['HeT410P80'].metadata['citation']), str(material_library['SiC'].metadata['citation'])]
    constituentCitation=" ".join(constituentCitationList)
    FNSFDCLL_mat.metadata['constituentcitation']=constituentCitation
    print('FNSFDCLL_mat  ', FNSFDCLL_mat.metadata['mat_number'], FNSFDCLL_mat.density)
    print("   Constituent Citations: ", constituentCitation)
    FNSFDCLL_mat=FNSFDCLL_mat.expand_elements()
    return FNSFDCLL_mat

# EUDEMO
# fullreference EadeFusEngDes_2017
# T. Eade et al., Fusion Engineering and Design 124 (2017) page 1241-1245
#    http://dx.doi.org/10.1016/j.fusengdes.2017.02.100
# fullreference GilbertNucFus_2017
# M. Gilbert et al., Nucl. Fusion 57 (2017) 046015
#    https://doi.org/10.1088/1741-4326/aa5bd7
#
# fullreference ZhouEnergies_2023
# G. Zhou et al., Energies 2023, 16, 5377
#    https://doi.org/10.3390/en16145377
#note: latest design uses mixed pebbles Li4SiO4+35 mole% Li2TiO3 and Be12Ti blocks

"""
EUDEMOHCPB 11.8% Eurofer,37.9% Be,13% Li4SiO4 (60% Li-6),8.7% He80bar,28.6% He1bar
"""
def mix_EUDEMOHCPB(material_library):
    mix=MultiMaterial({material_library['EUROFER97']:0.118, material_library['Be']:0.379, material_library['Li4SiO4Li60']:0.13, material_library['HeT410P80']: 0.087, material_library['HeT410P1']: 0.286})
    EUDEMOHCPB_mat=mix.mix_by_volume()
    EUDEMOHCPB_mat.metadata['mat_number']=221
    EUDEMOHCPB_mat.metadata['mixturecitation']='EadeFusEngDes_2017'
    constituentCitationList=[str(material_library['EUROFER97'].metadata['citation']), str(material_library['Be'].metadata['citation']), str(material_library['Li4SiO4Li60'].metadata['citation']), str(material_library['HeT410P80'].metadata['citation']), str(material_library['HeT410P1'].metadata['citation'])]
    constituentCitation=" ".join(constituentCitationList)
    EUDEMOHCPB_mat.metadata['constituentcitation']=constituentCitation
    print('EUDEMOHCPB_mat  ', EUDEMOHCPB_mat.metadata['mat_number'], EUDEMOHCPB_mat.density)
    print("   Constituent Citations: ", constituentCitation)
    EUDEMOHCPB_mat=EUDEMOHCPB_mat.expand_elements()
    return EUDEMOHCPB_mat

"""
EUDEMOHCPBacb 11.8% Eurofer,37.9% Be,8.45% Li4SiO4 (60% Li-6),4.55% Li2TiO3 (60% Li-6),8.7% He80bar,28.6% He1bar
"""
def mix_EUDEMOHCPBacb(material_library):
    mix=MultiMaterial({material_library['EUROFER97']:0.118, material_library['Be12Ti']:0.379, material_library['Li4SiO4Li60']:0.0845, material_library['Li2TiO3Li60']:0.0455, material_library['HeT410P80']: 0.087, material_library['HeT410P1']: 0.286})
    EUDEMOHCPBacb_mat=mix.mix_by_volume()
    EUDEMOHCPBacb_mat.metadata['mat_number']=222
    EUDEMOHCPBacb_mat.metadata['mixturecitation']='ZhouEnergies_2023 and ???'
    constituentCitationList=[str(material_library['EUROFER97'].metadata['citation']), str(material_library['Be12Ti'].metadata['citation']), str(material_library['Li4SiO4Li60'].metadata['citation']), str(material_library['Li2TiO3Li60'].metadata['citation']), str(material_library['HeT410P80'].metadata['citation']), str(material_library['HeT410P1'].metadata['citation'])]
    constituentCitation=" ".join(constituentCitationList)
    EUDEMOHCPBacb_mat.metadata['constituentcitation']=constituentCitation
    print('EUDEMOHCPBacb_mat  ', EUDEMOHCPBacb_mat.metadata['mat_number'], EUDEMOHCPBacb_mat.density)
    print("   Constituent Citations: ", constituentCitation)
    EUDEMOHCPBacb_mat=EUDEMOHCPBacb_mat.expand_elements()
    return EUDEMOHCPBacb_mat

# generic breeder materials

"""
PbLi90BZ 100% LiPb (90% Li-6)
"""
def mix_PbLi90BZ(material_library):
    mix=MultiMaterial({material_library['Pb157Li90']:1.00})
    PbLi90BZ_mat=mix.mix_by_volume()
    PbLi90BZ_mat.metadata['mat_number']=223
    PbLi90BZ_mat.metadata['mixturecitation']='ARIES and MELCOR TMAP'
    print('PbLi90BZ_mat  ', PbLi90BZ_mat.metadata['mat_number'], PbLi90BZ_mat.density)
    PbLi90BZ_mat=PbLi90BZ_mat.expand_elements()
    return PbLi90BZ_mat

"""
FlibeLi60BZ 100% Flibe (60% Li-6)
"""
def mix_FlibeLi60BZ(material_library):
    mix=MultiMaterial({material_library['FlibeLi60']:1.00})
    FlibeLi60BZ_mat=mix.mix_by_volume()
    FlibeLi60BZ_mat.metadata['mat_number']=224
    FlibeLi60BZ_mat.metadata['mixturecitation']='BoullonFusEngDes_2017 and density ???'
    print('FlibeLi60BZ_mat  ', FlibeLi60BZ_mat.metadata['mat_number'], FlibeLi60BZ_mat.density)
    FlibeLi60BZ_mat=FlibeLi60BZ_mat.expand_elements()
    return FlibeLi60BZ_mat

# shielding 

"""
FNSFIBSR (28% MF82H, 20% He, 52% WC filler) 
"""
# fullreference
def mix_FNSFIBSR(material_library):
    mix=MultiMaterial({material_library['MF82H']:0.28, material_library['WC']:0.52, material_library['HeT410P80']: 0.20})
    FNSFIBSR_mat=mix.mix_by_volume()
    FNSFIBSR_mat.metadata['mat_number']=2
    FNSFIBSR_mat.metadata['mixturecitation']='ElGuebalyFusSciTec_2017 and Others'
    print('FNSFIBSR_mat  ', FNSFIBSR_mat.metadata['mat_number'], FNSFIBSR_mat.density)
    FNSFIBSR_mat=FNSFIBSR_mat.expand_elements()
    return FNSFIBSR_mat

"""
FNSFIBSRstruct    (100% FS MF82H)
"""
def mix_FNSFIBSRstruct(material_library):
    mix=MultiMaterial({material_library['MF82H']:1.00})
    FNSFIBSRstruct_mat=mix.mix_by_volume()
    FNSFIBSRstruct_mat.metadata['mat_number']=400
    FNSFIBSRstruct_mat.metadata['mixturecitation']='SchnabelNDS2024'
    print('FNSFIBSRstruct_mat  ', FNSFIBSRstruct_mat.metadata['mat_number'], FNSFIBSRstruct_mat.density)
    FNSFIBSRstruct_mat=FNSFIBSRstruct_mat.expand_elements()
    return FNSFIBSRstruct_mat

"""
FNSFIBSRfill
"""
def mix_FNSFIBSRfill(material_library):
    mix=MultiMaterial({material_library['MF82H']:0.05, material_library['WC']:0.686, material_library['HeT410P80']: 0.264})
    FNSFIBSRfill_mat=mix.mix_by_volume()
    FNSFIBSRfill_mat.metadata['mat_number']=401
    FNSFIBSRfill_mat.metadata['mixturecitation']='SchnabelNDS2024'
    print('FNSFIBSRfill_mat  ', FNSFIBSRfill_mat.metadata['mat_number'], FNSFIBSRfill_mat.density)
    FNSFIBSRfill_mat=FNSFIBSRfill_mat.expand_elements()
    return FNSFIBSRfill_mat

"""
FNSFCC    (100% SS316LN closest to SS316LNIG)
"""
def mix_FNSFCC(material_library):
    mix=MultiMaterial({material_library['SS316LNIG']:1.00})
    FNSFCC_mat=mix.mix_by_volume()
    FNSFCC_mat.metadata['mat_number']=17
    FNSFCC_mat.metadata['mixturecitation']='DavisFusEngDes_2018'
    print('FNSFCC_mat  ', FNSFCC_mat.metadata['mat_number'], FNSFCC_mat.density)
    FNSFCC_mat=FNSFCC_mat.expand_elements()
    return FNSFCC_mat
    
"""
FNSFIBWP (29% JK2LB Steel, 43% Cu, 6% Ternary Nb3Sn, 8% Hybrid Electric Insulator, 14% Liquid He)
"""
def mix_FNSFIBWP(material_library):
    mix=MultiMaterial({material_library['JK2LBSteel']:0.29, material_library['Cu']:0.43, material_library['TernaryNb3Sn']:0.06, material_library['Eins']:0.08, material_library['LHe']:0.14})
    FNSFIBWP_mat=mix.mix_by_volume()
    FNSFIBWP_mat.metadata['mat_number']=19
    FNSFIBWP_mat.metadata['mixturecitation']='SchnabelNDS2024'
    print('FNSFIBWP_mat  ', FNSFIBWP_mat.metadata['mat_number'], FNSFIBWP_mat.density)
    FNSFIBWP_mat=FNSFIBWP_mat.expand_elements()
    return FNSFIBWP_mat

"""
IFMIFDONESspecimenstack    (75% EUROFER97, 25% Na)
"""
# fullreference QiuNucMatEnergy_2018 https://doi.org/10.1016/j.nme.2018.04.009
def mix_IFMIFDONESspecimenstack(material_library):
    mix=MultiMaterial({material_library['EUROFER97']:0.75,material_library['Na']:0.25})
    IFMIFDONESspecimenstack_mat=mix.mix_by_volume()
    IFMIFDONESspecimenstack_mat.metadata['mat_number']=29
    IFMIFDONESspecimenstack_mat.metadata['mixturecitation']='QiuNucMatEnergy_2018'
    constituentCitationList=[str(material_library['EUROFER97'].metadata['citation']),str(material_library['Na'].metadata['citation'])]
    constituentCitation=" ".join(constituentCitationList)
    IFMIFDONESspecimenstack_mat.metadata['constituentcitation']=constituentCitation
    print('IFMIFDONESspecimenstack_mat  ', IFMIFDONESspecimenstack_mat.metadata['mat_number'], IFMIFDONESspecimenstack_mat.density)
    print ('   Constituent Citations: ', constituentCitation)
    IFMIFDONESspecimenstack_mat=IFMIFDONESspecimenstack_mat.expand_elements()
    return IFMIFDONESspecimenstack_mat

def mix_Pb(material_library):
    mix=MultiMaterial({material_library['Pb']:1.00})
    Pb_mat=mix.mix_by_volume()
    Pb_mat.metadata['mat_number']=30
    Pb_mat.metadata['mixturecitation']=str(material_library['Pb'].metadata['citation'])
    print('Pb_mat  ', Pb_mat.metadata['mat_number'], Pb_mat.density) 
    Pb_mat=Pb_mat.expand_elements()
    return Pb_mat

def mix_SS316LN(material_library):
    mix=MultiMaterial({material_library['SS316LN']:1.00})
    SS316LN_mat=mix.mix_by_volume()
    SS316LN_mat.metadata['mat_number']=32
    SS316LN_mat.metadata['mixturecitation']=str(material_library['SS316LN'].metadata['citation'])
    print('SS316LN_mat  ', SS316LN_mat.metadata['mat_number'], SS316LN_mat.density) 
    SS316LN_mat=SS316LN_mat.expand_elements()
    return SS316LN_mat

def mix_Concrete(material_library):
    mix=MultiMaterial({material_library['Concrete']:1.00})
    Concrete_mat=mix.mix_by_volume()
    Concrete_mat.metadata['mat_number']=31
    Concrete_mat.metadata['mixturecitation']=str(material_library['Concrete'].metadata['citation'])
    print('Concrete_mat  ', Concrete_mat.metadata['mat_number'], Concrete_mat.density) 
    Concrete_mat=Concrete_mat.expand_elements()
    return Concrete_mat

#  J.-C. Jaboulay, G. Aiello, J. Aubert, and R. Boullon https://doi.org/10.1016/j.fusengdes.2018.12.008
def mix_HCCL_cap_advanced_plus(material_library):
    
    mix=MultiMaterial({material_library['EUROFER97']:0.97,
                       material_library['HeT410P80']:0.03})
    cap_mat = mix.mix_by_volume()
    
    cap_mat.metadata['mat_number'] = 33
    cap_mat.metadata['mixturecitation']='https://doi.org/10.1016/j.fusengdes.2018.12.008'
    
    constituentCitationList=[str(material_library['EUROFER97'].metadata['citation']),
                             str(material_library['HeT410P80'].metadata['citation'])]
    constituentCitation=" ".join(constituentCitationList)
    cap_mat.metadata['constituentcitation'] = constituentCitation
    
    print('HCLL Advanced Plus Cap_mat', cap_mat.metadata['mat_number'],cap_mat.density)
    print('   Constituent Citations: ', constituentCitation)
    
    cap_mat = cap_mat.expand_elements()
    return(cap_mat)

# R. Boullon, J. Aubert, G. Aiello, J.-C. Jaboulay, A. Morin, and J. Peyraud https://doi.org/10.1016/j.fusengdes.2018.04.107
def mix_HCLL_advanced_plus_breeder_mat(material_library):
    
    mix=MultiMaterial({material_library['EUROFER97']:0.066,
                       material_library['HeT410P80']:0.044, 
                       material_library['Pb157Li90']:0.89})
    HCLL_BZ_mat = mix.mix_by_volume()
    
    HCLL_BZ_mat.metadata['mat_number'] = 34
    HCLL_BZ_mat.metadata['mixturecitation']='https://doi.org/10.1016/j.fusengdes.2018.04.107'
   
    constituentCitationList=[str(material_library['EUROFER97'].metadata['citation']),
                             str(material_library['HeT410P80'].metadata['citation']),
                             str(material_library['Pb157Li90'])]
    constituentCitation=" ".join(constituentCitationList)
    HCLL_BZ_mat.metadata['constituentcitation']= constituentCitation
    
    print('HCLL Breeder mat', HCLL_BZ_mat.metadata['mat_number'],
          HCLL_BZ_mat.density)
    print('   Constituent Citations: ', constituentCitation)
    
    HCLL_BZ_mat = HCLL_BZ_mat.expand_elements()
    return HCLL_BZ_mat

#  J.-C. Jaboulay, G. Aiello, J. Aubert, and R. Boullon https://doi.org/10.1016/j.fusengdes.2018.12.008
def mix_HCLL_FW(material_library):
    
    w_fraction = 0.2/2.7
    fw_fraction = 1-w_fraction
    mix = MultiMaterial({material_library['W']:w_fraction,
                         material_library['EUROFER97']:0.71*fw_fraction,
                         material_library['HeT410P80']:0.29*fw_fraction})
    HCLL_FW_mat = mix.mix_by_volume()

    HCLL_FW_mat.metadata['mat_number'] = 35
    HCLL_FW_mat.metadata['mixturecitation']="https://doi.org/10.1016/j.fusengdes.2018.12.008"
    
    constituentCitationList = [str(material_library['EUROFER97'].metadata['citation']),
                             str(material_library['HeT410P80'].metadata['citation']),
                             str(material_library['W'].metadata['citation'])]
    constituentCitation = " ".join(constituentCitationList)
    HCLL_FW_mat.metadata['constituentcitation'] = constituentCitation

    print('HCLL FW mat',HCLL_FW_mat.metadata['mat_number'], HCLL_FW_mat.density)
    print("   Constituent Citations: ", constituentCitation)
    HCLL_FW_mat = HCLL_FW_mat.expand_elements()
    return HCLL_FW_mat

# R. Boullon, J. Aubert, G. Aiello, J.-C. Jaboulay, A. Morin, and J. Peyraud https://doi.org/10.1016/j.fusengdes.2018.04.107
def mix_HCLL_advanced_plus_breeder_MMS(material_library):
    
    breeder = mix_HCLL_advanced_plus_breeder_mat(material_library)
    side_wall = mix_HCLL_FW(material_library)
    cap = mix_HCCL_cap_advanced_plus(material_library)

    mix = MultiMaterial({breeder:0.888, side_wall:0.035, cap:0.077})
    HCLL_BZ = mix.mix_by_volume()

    HCLL_BZ.metadata['mat_number'] = 36
    HCLL_BZ.metadata['mixturecitation'] = "derived from dimensions in https://doi.org/10.1016/j.fusengdes.2018.04.107"
    
    constituentCitationList = [str(breeder.metadata['citation']),
                             str(side_wall.metadata['citation']),
                             str(cap.metadata['citation'])]
    constituentCitation = " ".join(constituentCitationList)
    HCLL_BZ.metadata['constituentcitation'] = constituentCitation

    print('HCLL BZ mat',HCLL_BZ.metadata['mat_number'], HCLL_BZ.density)
    print("   Constituent Citations: ", constituentCitation)

    return HCLL_BZ
    

########################################################################    
def main():
    #
    # remove old mixmat_lib
    try: 
        os.remove("mixedPureFusionMaterials_libv1.h5")
    except: 
        pass  
    # create material library object
    mixmat_lib = MaterialLibrary()
           
    # Load material library
    mat_lib=load_matlib()

    # mix FNSFFW
    FNSFFW_mat = mix_FNSFFW(mat_lib)
    mixmat_lib['FNSFFW']= FNSFFW_mat

    FNSFFWstruct_mat = mix_FNSFFWstruct(mat_lib)
    mixmat_lib['FNSFFWstruct']= FNSFFWstruct_mat

    # mix reIron
    reIron_mat = mix_reIron(mat_lib)
    mixmat_lib['reIron']= reIron_mat

    # blanket materials
    FNSFDCLL_mat = mix_FNSFDCLL(mat_lib)
    mixmat_lib['FNSFDCLL']= FNSFDCLL_mat

    EUDEMOHCPB_mat = mix_EUDEMOHCPB(mat_lib)
    mixmat_lib['EUDEMOHCPB']= EUDEMOHCPB_mat

    EUDEMOHCPBacb_mat = mix_EUDEMOHCPBacb(mat_lib)
    mixmat_lib['EUDEMOHCPBacb']= EUDEMOHCPBacb_mat    
    
    PbLi90BZ_mat = mix_PbLi90BZ(mat_lib)
    mixmat_lib['PbLi90BZ']= PbLi90BZ_mat
    FlibeLi60BZ_mat = mix_FlibeLi60BZ(mat_lib)
    mixmat_lib['FlibeLi60BZ']= FlibeLi60BZ_mat
    
    # homogenized shields
    FNSFIBSR_mat = mix_FNSFIBSR(mat_lib)
    mixmat_lib['FNSFIBSR']= FNSFIBSR_mat

    # shield fillers
    FNSFIBSRfill_mat = mix_FNSFIBSRfill(mat_lib)
    mixmat_lib['FNSFIBSRfill']= FNSFIBSRfill_mat

    # shield structure or shell
    FNSFIBSRstruct_mat = mix_FNSFIBSRstruct(mat_lib)
    mixmat_lib['FNSFIBSRstruct']= FNSFIBSRstruct_mat

    # magnets
    FNSFCC_mat = mix_FNSFCC(mat_lib)
    mixmat_lib['FNSFCC']= FNSFCC_mat
    FNSFIBWP_mat = mix_FNSFIBWP(mat_lib)
    mixmat_lib['FNSFIBWP']= FNSFIBWP_mat

    # other 
    IFMIFDONESspecimenstack_mat = mix_IFMIFDONESspecimenstack(mat_lib)
    mixmat_lib['IFMIFDONESspecimenstack']= IFMIFDONESspecimenstack_mat
    
    Pb_mat = mix_Pb(mat_lib)
    mixmat_lib['Pb']= Pb_mat

    Concrete_mat = mix_Concrete(mat_lib)
    mixmat_lib['Concrete']= Concrete_mat

    SS316LN_mat = mix_SS316LN(mat_lib)
    mixmat_lib['SS316LN']= SS316LN_mat

    HCLL_breeder = mix_HCLL_advanced_plus_breeder_MMS(mat_lib)
    mixmat_lib['HCLLMMSBZ'] = HCLL_breeder

    HCLLFW = mix_HCLL_FW(mat_lib)
    mixmat_lib['HCLLFW'] = HCLLFW
    
    # write fnsf material library
    mixmat_lib.write_hdf5("mixedPureFusionMaterials_libv1.h5") # don't set datapath,nucpath...will be pyne default values
    # change datapath to be able to read with older version of uwuw_preproc
    #mixmat_lib.write_hdf5("mixedPureFusionMaterials_libv1_old.h5",datapath='/materials', nucpath='/nucid')

if __name__ == "__main__":
    main()

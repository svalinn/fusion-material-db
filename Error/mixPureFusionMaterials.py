#! /usr/bin/python
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
from pyne.material import Material, MaterialLibrary, MultiMaterial
#
# Load material library (created using pyne)

def load_matlib():
    mat_lib=MaterialLibrary()
    mat_lib.from_hdf5("PureFusionMaterials_libv1.h5") # don't set datapath,nucpath...will be pyne default values
    return mat_lib
   
# Mix Materials by Volume

"""
FNSFFW    (34% FS MF82H, 66% He)
"""
# reference DavisFusEngDes_2018 https://doi.org/10.1016/j.fusengdes.2017.06.008
def mix_FNSFFW(material_library):
    mix=MultiMaterial({material_library['MF82H']:0.34,material_library['HeT410P80']:0.66})
    FNSFFW_mat=mix.mix_by_volume()
    FNSFFW_mat.metadata['mat_number']=9
    FNSFFW_mat.metadata['mixturecitation']='DavisFusEngDes_2018'
    constituentCitationList=[str(material_library['MF82H'].metadata['citation']),str(material_library['HeT410P80'].metadata['citation'])]
    constituentCitation=" ".join(constituentCitationList)
    FNSFFW_mat.metadata['constituentcitation']=constituentCitation
    print 'FNSFFW_mat  ', FNSFFW_mat.metadata['mat_number'], FNSFFW_mat.density
    print "   Constituent Citations: ", constituentCitation
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
    print 'FNSFFWstruct_mat  ', FNSFFWstruct_mat.metadata['mat_number'], FNSFFWstruct_mat.density
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
    print 'reIron_mat  ', reIron_mat.metadata['mat_number'], reIron_mat.density 
    reIron_mat=reIron_mat.expand_elements()
    return reIron_mat
#
# blanket materials

#FNSF OB DCLL Blanket (73.7% LiPb (90% Li-6), 14.9% He/void, 7.5% FS, 3.9% SiC)
# reference EliasUWFMD1424_2015 https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1424.pdf
#FNSF IB DCLL Blanket (80% LiPb (90% Li-6), 12% He/void, 5% FS, 3% SiC)
# reference MadaniUWFDM1423_2015 https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1423.pdf

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
    print 'FNSFDCLL_mat  ', FNSFDCLL_mat.metadata['mat_number'], FNSFDCLL_mat.density
    print "   Constituent Citations: ", constituentCitation
    FNSFDCLL_mat=FNSFDCLL_mat.expand_elements()
    return FNSFDCLL_mat

# EUDEMO
# reference EadeFusEngDes_2017
# T. Eade et al., Fusion Engineering and Design 124 (2017) page 1241-1245
#    http://dx.doi.org/10.1016/j.fusengdes.2017.02.100
# reference GilbertNucFus_2017
# M. Gilbert et al., Nucl. Fusion 57 (2017) 046015
#    https://doi.org/10.1088/1741-4326/aa5bd7
#
# reference ZhouEnergies_2023
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
    print 'EUDEMOHCPB_mat  ', EUDEMOHCPB_mat.metadata['mat_number'], EUDEMOHCPB_mat.density
    print "   Constituent Citations: ", constituentCitation
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
    print 'EUDEMOHCPBacb_mat  ', EUDEMOHCPBacb_mat.metadata['mat_number'], EUDEMOHCPBacb_mat.density
    print "   Constituent Citations: ", constituentCitation
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
    print 'PbLi90BZ_mat  ', PbLi90BZ_mat.metadata['mat_number'], PbLi90BZ_mat.density
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
    print 'FlibeLi60BZ_mat  ', FlibeLi60BZ_mat.metadata['mat_number'], FlibeLi60BZ_mat.density
    FlibeLi60BZ_mat=FlibeLi60BZ_mat.expand_elements()
    return FlibeLi60BZ_mat

# shielding 

"""
FNSFIBSR (28% MF82H, 20% He, 52% WC filler) 
"""
# reference
def mix_FNSFIBSR(material_library):
    mix=MultiMaterial({material_library['MF82H']:0.28, material_library['WC']:0.52, material_library['HeT410P80']: 0.20})
    FNSFIBSR_mat=mix.mix_by_volume()
    FNSFIBSR_mat.metadata['mat_number']=2
    FNSFIBSR_mat.metadata['mixturecitation']='ElGuebalyFusSciTec_2017 and Others'
    print 'FNSFIBSR_mat  ', FNSFIBSR_mat.metadata['mat_number'], FNSFIBSR_mat.density
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
    print 'FNSFIBSRstruct_mat  ', FNSFIBSRstruct_mat.metadata['mat_number'], FNSFIBSRstruct_mat.density
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
    print 'FNSFIBSRfill_mat  ', FNSFIBSRfill_mat.metadata['mat_number'], FNSFIBSRfill_mat.density
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
    print 'FNSFCC_mat  ', FNSFCC_mat.metadata['mat_number'], FNSFCC_mat.density
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
    print 'FNSFIBWP_mat  ', FNSFIBWP_mat.metadata['mat_number'], FNSFIBWP_mat.density
    FNSFIBWP_mat=FNSFIBWP_mat.expand_elements()
    return FNSFIBWP_mat

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

    
    # write fnsf material library
    mixmat_lib.write_hdf5("mixedPureFusionMaterials_libv1.h5") # don't set datapath,nucpath...will be pyne default values
    # change datapath to be able to read with older version of uwuw_preproc
    mixmat_lib.write_hdf5("mixedPureFusionMaterials_libv1_old.h5",datapath='/materials', nucpath='/nucid')

if __name__ == "__main__":
    main()

#! /usr/bin/python
#
# pure fusion materials based on FESS-FNSF, ARIES, EU-DEMO
# -can be used for mixing homogenized regions
# -generally impurities at <~1e-3 wt. percent (10 wppm) are removed from materials
#   (except SS-316 steels may contain boron impurity)
# 
#
import os
from pyne import material
from pyne.material import Material, MaterialLibrary, MultiMaterial
#
#
# reference: KluehJNM_2000 R.L. Klueh et al. jnm 2000 DOI:10.1016/S0022-3115(00)00060-X
def MF82H_mat() :
    nucvec = {60000000: 0.1, 230000000: 0.2, 240000000: 7.5, 260000000: 90.18, 730000000: 0.02, 740000000: 2.0}
    MF82H = Material(nucvec)
    MF82H.density = 7.89
    MF82H=MF82H.expand_elements()
    MF82H.metadata['citation']='KluehJNM_2000'
    return MF82H

# reference: MergiaJNM_2008 K. Mergia, N. Boukos jnm 2008 https://doi.org/10.1016/j.jnucmat.2007.03.267
# wt percent  0.11C, 8.9Cr, 0.42Mn, 0.19V, 1.10W, 0.14Ta, balance Fe
def EUROFER97_mat() :
    nucvec = {60000000: 0.11, 230000000: 0.19, 240000000: 8.9, 250000000: 0.42, 260000000: 89.14, 730000000: 0.14, 740000000: 1.10}
    EUROFER97 = Material(nucvec)
    EUROFER97.density = 7.75
    EUROFER97=EUROFER97.expand_elements()
    EUROFER97.metadata['citation']='MergiaJNM_2008'
    return EUROFER97
    
# reference: KluehJNM_2000 MF82H with 3 wt. percent B replacing some Fe
def BMF82H_mat() :
    nucvec = {50000000: 3.0, 60000000: 0.1, 230000000: 0.2, 240000000: 7.5, 260000000: 87.18, 730000000: 0.02, 740000000: 2.0}
    BMF82H = Material(nucvec)
    BMF82H.density = 7.89
    BMF82H=BMF82H.expand_elements()
    BMF82H.metadata['citation']='KluehJNM_2000'
    return BMF82H

# reference: aries.ucsd.edu/PROPS/ITER/AM01/AM01-1100.html
# reference: CRChandbook64   bulk density of WC: 64th CRC Handbook of Chemistry and Physics, B-152
def WC_mat():
    nucvec = {60000000:6.13,740000000:93.87}          
    WC = Material(nucvec)
    WC.density = 15.63
    WC=WC.expand_elements()
    WC.metadata['citation']='CRChandbook64B152'
    return WC

# reference: pnnl-15870rev1 R.J. McConn, et al. "Compendium of Material Composition Data for Radiation Transport Modeling", PNNL-15870 Rev. 1, 2011.
def Water_mat() :
    nucvec = {10000000: 11.1894, 80000000: 88.8106}
    Water = Material(nucvec)
    Water.density = 1.0
    Water=Water.expand_elements()
    Water.metadata['citation']='pnnl-15870rev1'
    return Water

# reference: BohmFusSciTec_2019 https://doi.org/10.1080/15361055.2019.1600930
# reference: MartelliFusEngDes_2019 https://doi.org/10.1016/j.fusengdes.2018.11.028
def Pb157Li90_mat() :
    nucvec = {30060000: 0.4905, 30070000: 0.0545,820000000: 99.455}
    Pb157Li90 = Material(nucvec)
    Pb157Li90.density = 9.32 # not sure of T
    Pb157Li90.molecular_mass = 175.6273
    Pb157Li90=Pb157Li90.expand_elements()
    Pb157Li90.metadata['citation']='BohmFusSciTec_2019'
    return Pb157Li90

# reference: pnnl-15870rev1
def SiC_mat() :
    nucvec = {60000000  : 29.9547, 140000000: 70.0453}
    SiC = Material(nucvec)
    SiC.density = 3.21
    SiC=SiC.expand_elements()
    SiC.metadata['citation']='pnnl-15870rev1'
    return SiC

# note SS-316L(N)-IG and EUROFER composition (but not density) in
# reference: GilbertNucFus_2017
# M. Gilbert et al., Nucl. Fusion 57 (2017) 046015
#    https://doi.org/10.1088/1741-4326/aa5bd7
#
# more extensive collection of ITER materials composition but not density
# reference: GilbertHandbookITERCCFE_2016 M. Gilbert, et al., "Handbook of activation, transmutation, and radiation damage properties of the elements and of ITER materials simulated using FISPACT-II & TENDL-2015; ITER FW armour focus", CCFE-R(16)37, September 2016. https://fispact.ukaea.uk/wp-content/uploads/2016/10/CCFE-R1637.pdf

# reference: GilbertHandbookITERCCFE_2016
# contains 300 wppm B which is important to assess typical He production level
def SS316LN_mat() :
    nucvec = {50000000:0.030, 60000000:0.030, 70000000:0.160, 140000000:1.0, 150000000:0.030, 160000000:0.020, 240000000:17.250, 250000000:2.00 , 260000000:64.830, 270000000:0.100, 280000000:12.00, 410000000:0.050, 420000000:2.5}
    SS316LN = Material(nucvec)
    SS316LN.density = 7.93
    SS316LN=SS316LN.expand_elements()
    SS316LN.metadata['citation']='GilbertHandbookITERCCFE_2016'
    return SS316LN

# reference: GilbertHandbookITERCCFE_2016 10 wppm B which is important to assess typical He production level
def SS316LNIG_mat() :
    nucvec = {50000000:0.001, 60000000:0.03, 70000000:0.070, 140000000:0.50, 150000000:0.025, 160000000:0.010, 220000000:0.10, 240000000:17.50, 250000000:1.80, 260000000:64.844, 270000000:0.05, 280000000:12.25, 290000000:0.30, 410000000:0.010, 420000000:2.5, 730000000:0.01}
    SS316LNIG = Material(nucvec)
    SS316LNIG.density = 7.93
    SS316LNIG=SS316LNIG.expand_elements()
    SS316LNIG.metadata['citation']='GilbertHandbookITERCCFE_2016'
    return SS316LNIG

# reference: pnnl-15870rev1
# added 10 wppm B which is important to assess typical He production level
def SS316L_mat() :
    nucvec = {50000000:0.001, 60000000:0.03, 140000000:1.0, 150000000:0.045, 160000000:0.03, 240000000:17, 250000000:2, 260000000:65.394, 280000000:12, 420000000:2.5}
    SS316L = Material(nucvec)
    SS316L.density = 8.00
    SS316L=SS316L.expand_elements()
    SS316L.metadata['citation']='pnnl-15870rev1'
    return SS316L

# reference: FESS-FNSF??? very similar to GFFpolyimide from ARIES
def Eins_mat() :
    nucvec = {10000000:1.96, 60000000:24.12, 70000000:1.46, 80000000:40.19, 120000000:3.92, 130000000: 8.6, 140000000:19.75}
    Eins = Material(nucvec)
    Eins.density = 1.8
    Eins=Eins.expand_elements()
    Eins.metadata['citation']='FESS-FNSF and ARIES GFFpolyimide'
    return Eins

# reference: ElGuebalyARIESCSFTI_2006 L. El-Guebaly, "Final Radial Build and Composition for LiPb/FS/He System", Sep. 2006. https://fti.neep.wisc.edu/fti.neep.wisc.edu/aries/BUILD-CS/build092606.pdf
# reference: P. Heizenroeder and R. Reed "Comments on Selection of U.S. ITER CS Coil Jacket Material"
def JK2LBSteel_mat() :
    nucvec = {50000000:0.002, 60000000:0.02, 70000000:0.2, 140000000:0.3, 150000000:0.004, 160000000:0.004, 240000000:13, 250000000:21, 260000000:55.47, 280000000:9, 420000000:1}
    JK2LBSteel = Material(nucvec)
    JK2LBSteel.density = 8.0
    JK2LBSteel=JK2LBSteel.expand_elements()
    JK2LBSteel.metadata['citation']='ElGuebalyARIESCSFTI_2006'
    return JK2LBSteel

# reference: FESS-FNSF and ???
def TernaryNb3Sn_mat() :
    nucvec = {410000000:68.95, 500000000:30, 220000000:1.05}
    TernaryNb3Sn = Material(nucvec)
    TernaryNb3Sn.density = 8.9
    TernaryNb3Sn=TernaryNb3Sn.expand_elements()
    TernaryNb3Sn.metadata['citation']='FESS-FNSF and ???'
    return TernaryNb3Sn  
 
# reference: ITER and CRC Handbook of Chemistry and Physics density at 4 K
# reference: CRChandbook64 64th CRC Handbook of Chemistry and Physics page B-117, density at 4 K
def LHe_mat() :
    nucvec = {20000000: 100}
    LHe = Material(nucvec)
    LHe.density = 0.149
    LHe=LHe.expand_elements()
    LHe.metadata['citation']='CRChandbook64B117'
    return LHe

# reference: maybe JawadORNL_2005 ???
# M. Jawad et al. , "Development of a New Class of Fe-3Cr-W(V) Ferritic Steels for Industrial Process Applications", ORNL/TM-2005/82, 2005. https://doi.org/10.2172/838517
def Cr3FS_mat() :
    nucvec = {60000:0.1, 140000:0.14, 230000:0.25, 240000:3.0, 250000:0.5, 260000:93.01, 740000:3.0}
    Cr3FS = Material(nucvec)
    Cr3FS.density = 7.89
    Cr3FS=Cr3FS.expand_elements()
    Cr3FS.metadata['citation']='JawadORNL_2005 and ???'
    return Cr3FS

# ODS LiPb-corrosion-resistant steel with Present impurities removed
# reference: PintDOE_ER_0313_57_2014 B. Pint et al., DEVELOPMENT OF ODS FeCrAl FOR FUSION REACTOR APPLICATIONS, Fusion Reactor Materials Program Semi-annual Report, Dec. 2014, DOE/ER- 0313/57  Section 2.1, https://fmp.ornl.gov/semiannual-progress-reports/fusion-materials-semiannual-progress-report-57.pdf
# reference: KluehJNM_2000 (for some impurities)
# Density = 7.799 g/cm3, as determined for 14YWT alloy, per David Hoelzer
#
def ODS125Y_mat() :
    nucvec = {60000000: 0.0380, 70000000:0.0455, 80000000:0.8420, 130000000:4.8, 140000000:0.02, 160000000:0.0020, 220000000:0.01, 240000000:11.4, 260000000:82.6025, 390000000:0.19, 740000000:0.05}
    ODS125Y = Material(nucvec)
    ODS125Y.density = 7.799
    ODS125Y=ODS125Y.expand_elements()
    ODS125Y.metadata['citation']='PintDOE_ER_0313_57_2014 and KluehJNM_2000 '
    return ODS125Y

# reference: pnnl-15870rev1 at T=20C
def D2O_mat() :
    nucvec = {10020000:20.1133, 80000000:79.8867}
    D2O = Material(nucvec)
    D2O.density = 1.10534
    D2O=D2O.expand_elements()
    D2O.metadata['citation']='pnnl-15870rev1'
    return D2O

# reference: WidodoJoPCS_2018 Journal of Physics Conference Series doi:10.1088/1742-6596/962/1/012039 and KTA Standards 1986
# also reference: pnnl-15870rev1
def HeNIST_mat() :
    nucvec = {20000000: 100}
    HeNIST = Material(nucvec)
    HeNIST.density = 0.00016647 # at 20 C (293.15 K), 1 atm (1.01325 bar)
    HeNIST=HeNIST.expand_elements()
    HeNIST.metadata['citation']='WidodoJoPCS_2018 and pnnl-15870rev1'
    return HeNIST

# high pressure He gas ref.
# reference: WidodoJoPCS_2018 doi:10.1088/1742-6596/962/1/012039 and KTA Standards 1986
def HeT410P1_mat() :
    nucvec = {20000000: 100}
    HeT410P1 = Material(nucvec)
    HeT410P1.density = 0.00007048 # at 410 C, 1 bar
    HeT410P1=HeT410P1.expand_elements()
    HeT410P1.metadata['citation']='WidodoJoPCS_2018'
    return HeT410P1

def HeT410P80_mat() :
    nucvec = {20000000: 100}
    HeT410P80 = Material(nucvec)
    HeT410P80.density = 0.00571698 # at 410 C, 80 bar
    HeT410P80=HeT410P80.expand_elements()
    HeT410P80.metadata['citation']='WidodoJoPCS_2018'
    return HeT410P80

# air (Dry, Near Sea Level)
# reference: pnnl-15870rev1
def AirSTP_mat() :
    nucvec = {60000000  : 0.0124, 70000000  : 75.5268, 80000000  : 23.1781, 180000000: 1.2827}
    AirSTP = Material(nucvec)
    AirSTP.density = 0.001205
    AirSTP=AirSTP.expand_elements()
    AirSTP.metadata['citation']='pnnl-15870rev1'
    return AirSTP

# concrete (Ordinary NBS 04)
# reference: pnnl-15870rev1
def Concrete_mat() :
    nucvec = {10000000  : 0.5558, 80000000  : 49.8076, 110000000: 1.7101, 120000000: 0.2565, 130000000: 4.5746, 140000000: 31.5092, 160000000: 0.1283, 190000000: 1.9239, 200000000: 8.2941, 260000000: 1.2398}
    Concrete = Material(nucvec)
    Concrete.density = 2.35
    Concrete=Concrete.expand_elements()
    Concrete.metadata['citation']='pnnl-15870rev1'
    return Concrete

# reference: pnnl-15870rev1
def W_mat() :
    nucvec = {740000000: 100.0}
    W = Material(nucvec=nucvec)
    W.density = 19.30
    W=W.expand_elements()
    W.metadata['citation']='pnnl-15870rev1'
    return W

# reference: pnnl-15870rev1
def Fe_mat() :
    nucvec = {260000000: 100.0}
    Fe = Material(nucvec=nucvec)
    Fe.density = 7.874
    Fe=Fe.expand_elements()
    Fe.metadata['citation']='pnnl-15870rev1'
    return Fe

# reference: pnnl-15870rev1 reactor graphite without boron impurity
def C_mat() :
    nucvec = {60000000:1.0}
    C = Material(nucvec)
    C.density = 1.7
    C=C.expand_elements()
    C.metadata['citation']='pnnl-15870rev1'
    return C

# reference: pnnl-15870rev1
def Si_mat() :
    nucvec = {140000000:1.0}
    Si = Material(nucvec)
    Si.density = 2.33
    Si=Si.expand_elements()
    Si.metadata['citation']='pnnl-15870rev1'
    return Si
    
# reference: pnnl-15870rev1
def Cu_mat() :
    nucvec = {290000000:1.0}
    Cu = Material(nucvec)
    Cu.density = 8.96
    Cu=Cu.expand_elements()
    Cu.metadata['citation']='pnnl-15870rev1'
    return Cu

# reference:  pnnl-15870rev1
def Sn_mat() :
    nucvec = {500000000:1.0}
    Sn = Material(nucvec)
    Sn.density = 7.31
    Sn=Sn.expand_elements()
    Sn.metadata['citation']='pnnl-15870rev1'
    return Sn

# reference: pnnl-15870rev1
def Ta_mat() :
    nucvec = {730000000:1.0}
    Ta = Material(nucvec)
    Ta.density = 16.654 
    Ta=Ta.expand_elements()
    Ta.metadata['citation']='pnnl-15870rev1'
    return Ta

# reference: pnnl-15870rev1
def Pb_mat() :
    nucvec = {820000000: 100.0}
    Pb = Material(nucvec=nucvec)
    Pb.density = 11.35
    Pb=Pb.expand_elements()
    Pb.metadata['citation']='pnnl-15870rev1'
    return Pb

# reference: HernandezFusEngDes_2018
# F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018
# https://doi.org/10.1016/j.fusengdes.2018.09.014
def Be_mat() :
    nucvec = {40000000:1.0}
    Be = Material(nucvec)
    Be.density = 1.85
    Be=Be.expand_elements()
    Be.metadata['citation']='HernandezFusEngDes_2018'
    return Be

# reference:  HernandezFusEngDes_2018
# F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018
# https://doi.org/10.1016/j.fusengdes.2018.09.014
def Be12Ti_mat():
    Be12Ti = Material()
    Be12Ti.from_atom_frac({40000000:12,220000000:1})
    Be12Ti.density = 2.28
    Be12Ti=Be12Ti.expand_elements()
    Be12Ti.metadata['citation']='HernandezFusEngDes_2018'
    return Be12Ti

# reference:  HernandezFusEngDes_2018
# F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018
# https://doi.org/10.1016/j.fusengdes.2018.09.014
def Be12V_mat():
    Be12V = Material()
    Be12V.from_atom_frac({40000000:12,230000000:1})
    Be12V.density = 2.39
    Be12V=Be12V.expand_elements()
    Be12V.metadata['citation']='HernandezFusEngDes_2018'
    return Be12V

# Li ceramics
# reference: HernandezFusEngDes_2018F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018 https://doi.org/10.1016/j.fusengdes.2018.09.014
# F.A. Hernandez, et al., Fusion Engineering and Design, Volume 157, 2020, 111614
# https://doi.org/10.1016/j.fusengdes.2020.111614
# ceramic breeders Li4SiO4 and Li2TiO3 at 60 wt. percent Li-6 EU-DEMO
# note manufacturing may result in lower density of 80-90% of theoretical

def Li4SiO4nat_mat():
    Li4SiO4nat= Material()
    Li4SiO4nat.from_atom_frac({30000000:4, 80000000:4, 140000000:1})
    Li4SiO4nat.density = 2.40
    Li4SiO4nat=Li4SiO4nat.expand_elements()
    Li4SiO4nat.metadata['citation']='HernandezFusEngDes_2018'
    return Li4SiO4nat

def Li2TiO3nat_mat():
    Li2TiO3nat= Material()
    Li2TiO3nat.from_atom_frac({30000000:2, 80000000:3, 220000000:1})
    Li2TiO3nat.density = 3.43
    Li2TiO3nat=Li2TiO3nat.expand_elements()
    Li2TiO3nat.metadata['citation']='HernandezFusEngDes_2018'
    return Li2TiO3nat

def Li4SiO4Li60_mat():
    Li4SiO4Li60= Material()
    li6enrichment=0.60 # weight fraction enrichment of Li-6 desired
    liXweightfraction = Material({'Li6': li6enrichment, 'Li7': (1.0-li6enrichment)})
    Li4SiO4Li60.from_atom_frac({liXweightfraction:4, 80000000:4, 140000000:1})
    Li4SiO4Li60.density = 2.40
    Li4SiO4Li60=Li4SiO4Li60.expand_elements()
    Li4SiO4Li60.metadata['citation']='HernandezFusEngDes_2018'
    return Li4SiO4Li60

def Li2TiO3Li60_mat():
    Li2TiO3Li60= Material()
    li6enrichment=0.60 # weight fraction enrichment of Li-6 desired
    liXweightfraction = Material({'Li6': li6enrichment, 'Li7': (1.0-li6enrichment)})
    Li2TiO3Li60.from_atom_frac({liXweightfraction:2, 80000000:3, 220000000:1})
    Li2TiO3Li60.density = 3.42
    Li2TiO3Li60=Li2TiO3Li60.expand_elements()
    Li2TiO3Li60.metadata['citation']='HernandezFusEngDes_2018'
    return Li2TiO3Li60

# reference: SohalINLEXT-10-18297_2013 M. Sohal et al., "Engineering Database of Liquid Salt Thermophysical and Thermochemical Properties", INL/EXT-10-18297, June 2013. https://inldigitallibrary.inl.gov/sites/STI/STI/5698704.pdf
def FlibeNat_mat():
    FlibeNat=Material()
    FlibeNat.from_atom_frac({30000000:2,40000000:1,90000000:4})
    FlibeNat.density=1.94
    FlibeNat=FlibeNat.expand_elements()
    FlibeNat.metadata['citation']='SohalINLEXT-10-18297_2013'
    return FlibeNat

# reference: SohalINLEXT-10-18297_2013 M. Sohal et al., "Engineering Database of Liquid Salt Thermophysical and Thermochemical Properties", INL/EXT-10-18297, June 2013. https://inldigitallibrary.inl.gov/sites/STI/STI/5698704.pdf
def FlibeLi60_mat():
    FlibeLi60=Material()
    li6enrichment=0.60 # weight fraction enrichment of Li-6 desired
    liXweightfraction = Material({'Li6': li6enrichment, 'Li7': (1.0-li6enrichment)})
    FlibeLi60.from_atom_frac({liXweightfraction:2,40000000:1,90000000:4})
    FlibeLi60.density=1.94
    FlibeLi60=FlibeLi60.expand_elements()
    FlibeLi60.metadata['citation']='SohalINLEXT-10-18297_2013'
    return FlibeLi60

# reference:  pnnl-15870rev1 at STP
def LiNat_mat() :
    nucvec = {30000000:1.0}
    LiNat = Material(nucvec)
    LiNat.density = 0.534 # at STP
    LiNat=LiNat.expand_elements()
    LiNat.metadata['citation']='pnnl-15870rev1'
    return LiNat

# reference: BohmFusSciTec_2019 rho=0.485 g/cm3 at T=500 C
def LiNatT500_mat() :
    nucvec = {30000000:1.0}
    LiNatT500 = Material(nucvec)
    LiNatT500.density = 0.485 # at T=500 C
    LiNatT500=LiNatT500.expand_elements()
    LiNatT500.metadata['citation']='BohmFusSciTec_2019'
    return LiNatT500

# reference:  pnnl-15870rev1
def Li60_mat() :
    Li60 = Material()
    li6enrichment=0.60 # weight fraction enrichment of Li-6 desired
    liXweightfraction = Material({'Li6': li6enrichment, 'Li7': (1.0-li6enrichment)})
    Li60.from_atom_frac({liXweightfraction:1})
    Li60.density = 0.534 # at STP
    Li60=Li60.expand_elements()
    Li60.metadata['citation']='pnnl-15870rev1'
    return Li60

# reference: BohmFusSciTec_2019 rho=0.485 g/cm3 at T=500 C
def Li60T500_mat() :
    Li60T500 = Material()
    li6enrichment=0.60 # weight fraction enrichment of Li-6 desired
    liXweightfraction = Material({'Li6': li6enrichment, 'Li7': (1.0-li6enrichment)})
    Li60T500.from_atom_frac({liXweightfraction:1})
    Li60T500.density = 0.485 # at T=500 C
    Li60T500=Li60T500.expand_elements()
    Li60T500.metadata['citation']='BohmFusSciTec_2019'
    return Li60T500

# --------------------------------------------------------
def main():
    # create material library object
    mat_lib = MaterialLibrary()
    print ("\n Creating Pure Fusion Materials...")
    #
    # get material definition
    mat_lib['MF82H']= MF82H_mat()
    mat_lib['EUROFER97']= EUROFER97_mat()
    mat_lib['BMF82H']= BMF82H_mat()
    mat_lib['WC'] = WC_mat()
    mat_lib['Water']= Water_mat()
    mat_lib['Pb157Li90']= Pb157Li90_mat()
    mat_lib['SiC']= SiC_mat()
    mat_lib['SS316LN']= SS316LN_mat()
    mat_lib['SS316LNIG']= SS316LNIG_mat()
    mat_lib['SS316L']= SS316L_mat()    
    mat_lib['Eins']=Eins_mat()
    mat_lib['JK2LBSteel']=JK2LBSteel_mat()
    mat_lib['TernaryNb3Sn']=TernaryNb3Sn_mat()
    mat_lib['LHe']= LHe_mat()
    mat_lib['Cr3FS']=Cr3FS_mat()
    mat_lib['ODS125Y']= ODS125Y_mat()
    mat_lib['D2O']= D2O_mat()
    mat_lib['HeNIST']= HeNIST_mat()
    mat_lib['HeT410P1']= HeT410P1_mat()
    mat_lib['HeT410P80']= HeT410P80_mat()
    mat_lib['AirSTP']= AirSTP_mat()
    mat_lib['Concrete']= Concrete_mat() 
    mat_lib['W']= W_mat()
    mat_lib['Fe']= Fe_mat()
    mat_lib['C']= C_mat()
    mat_lib['Si']= Si_mat()
    mat_lib['Cu']=Cu_mat()
    mat_lib['Sn']=Sn_mat()
    mat_lib['Ta']=Ta_mat()    
    mat_lib['Pb']=Pb_mat()
    mat_lib['Be']=Be_mat()
    mat_lib['Be12Ti']=Be12Ti_mat()    
    mat_lib['Be12V']=Be12V_mat()
    mat_lib['Li4SiO4nat']=Li4SiO4nat_mat()
    mat_lib['Li2TiO3nat']=Li2TiO3nat_mat()
    mat_lib['Li4SiO4Li60']=Li4SiO4Li60_mat()
    mat_lib['Li2TiO3Li60']=Li2TiO3Li60_mat()
    mat_lib['FlibeNat']=FlibeNat_mat()
    mat_lib['FlibeLi60']=FlibeLi60_mat()
    mat_lib['LiNat']=LiNat_mat()
    mat_lib['LiNatT500']=LiNatT500_mat()
    mat_lib['Li60']=Li60_mat()
    mat_lib['Li60T500']=Li60T500_mat()
    
    # remove lib
    try: 
        os.remove("PureFusionMaterials_libv1.h5")
    except: 
        pass  
        
    # write fnsf1d material library
    mat_lib.write_hdf5("PureFusionMaterials_libv1.h5") # don't set datapath,nucpath...will be pyne default values
    # change datapath to be able to read with older version of uwuw_preproc
    mat_lib.write_hdf5("PureFusionMaterials_libv1_old.h5",datapath='/materials', nucpath='/nucid')

    print ("All done!")
    
    
if __name__ == "__main__":
    main()

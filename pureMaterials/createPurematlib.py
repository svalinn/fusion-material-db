#! /usr/bin/python
#
# -updated for python3 (print) and updated for changes in python modules
#
# pure fusion materials based on FESS-FNSF, ARIES, EU-DEMO
# -can be used for mixing homogenized regions
# -generally impurities at <~1e-3 wt. percent (10 wppm) are removed from materials
#   (except SS-316 steels may contain boron impurity)
#
#
import os
from typing import Dict, Union, Optional
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary
from pyne import nucname
#
#


def enrich(
    nucvec: Dict[int, float], old_key: int, new_values: Dict[int, float]
) -> Dict[int, float]:
    """Update nuclear vector by replacing an old key with new key-value pairs."""

    if old_key in nucvec:
        fract = nucvec.pop(old_key)
        for key, value in new_values.items():
            nucvec[key] = value * fract
    else:
        found_key = None
        for key in list(nucvec.keys()):
            if nucname.id(old_key) == nucname.id(key):
                found_key = key
                break

        if found_key is not None:
            fract = nucvec.pop(found_key)
            for new_key, value in new_values.items():
                nucvec[new_key] = value * fract  # check if percent works also

    return nucvec


def make_mat(
    nucvec: Dict[int, float],
    density: float,
    citation: str,
    molecular_mass: Optional[float] = None,
    mass_enrichment: Optional[Dict[int, Dict[int, float]]] = None,
) -> Material:
    """Create a Material object from nuclear vector data."""
    if mass_enrichment:
        for element, enrichment_vector in mass_enrichment.items():
            enriched_mat = Material(enrichment_vector)
            nucvec = enrich(nucvec, element, enriched_mat.comp)
    mat = Material(nucvec, density=density, metadata={"citation": citation})
    if molecular_mass:
        mat.molecular_mass = molecular_mass
    return mat.expand_elements()


def make_mat_from_atom(
    atom_frac: Dict[Union[int, str], float],
    density: float,
    citation: str,
    mass_enrichment: Optional[Dict[int, Dict[int, float]]] = None,
) -> Material:
    """Create a Material object from atom fraction data."""
    if mass_enrichment:
        for element, enrichment_vector in mass_enrichment.items():
            enriched_mat = Material(enrichment_vector)
            atom_frac = enrich(atom_frac, element, enriched_mat.to_atom_frac())

    mat = Material()
    mat.from_atom_frac(atom_frac)
    mat.density = density
    mat.metadata["citation"] = citation
    return mat.expand_elements()

mat_data = {}

# fullreference: KluehJNM_2000 R.L. Klueh et al. jnm 2000 DOI:10.1016/S0022-3115(00)00060-X
mat_data["MF82H"] = {
    "nucvec": {
        60000000: 0.1,
        230000000: 0.2,
        240000000: 7.5,
        260000000: 90.18,
        730000000: 0.02,
        740000000: 2.0,
    },
    "density": 7.89,
    "citation": "KluehJNM_2000",
}

# fullreference: ChenNucEngTech_2013 Y. Chen Nuclear and Engineering Technology, vol. 45, 2013. https://doi.org/10.5516/NET.07.2013.706
# fullreference: SmithBCSSANLvol2_1984, D.L. Smith et al., "Blanket Comparison and Selection Study Final Report", ANL/FPP-84-1, volume 2, Chapter 6, 1984. (HT-9 density pdf page 32 and 49)
mat_data["HT9"] = {
    "nucvec": {
        60000000: 0.2,
        230000000: 0.25,
        240000000: 12.0,
        260000000: 85.55,
        280000000: 0.5,
        420000000: 1.0,
        740000000: 0.5,
    },
    "density": 7.8,  # density BCSSvol2 pdf page 32 and page 49
    "citation": "KluehJNM_2000 and SmithBCSSANLvol2_1984",
}

# fullreference: MergiaJNM_2008 K. Mergia, N. Boukos jnm 2008 https://doi.org/10.1016/j.jnucmat.2007.03.267
# wt percent  0.11C, 8.9Cr, 0.42Mn, 0.19V, 1.10W, 0.14Ta, balance Fe
mat_data["EUROFER97"] = {
    "nucvec": {
        60000000: 0.11,
        230000000: 0.19,
        240000000: 8.9,
        250000000: 0.42,
        260000000: 89.14,
        730000000: 0.14,
        740000000: 1.10,
    },
    "density": 7.75,
    "citation": "MergiaJNM_2008",
}

# reference: KluehJNM_2000 MF82H with 3 wt. percent B replacing some Fe
mat_data["BMF82H"] = {
    "nucvec": {
        50000000: 3.0,
        60000000: 0.1,
        230000000: 0.2,
        240000000: 7.5,
        260000000: 87.18,
        730000000: 0.02,
        740000000: 2.0,
    },
    "density": 7.89,
    "citation": "KluehJNM_2000",
}

# fullreference: pnnl-15870rev1 R.J. McConn, et al. "Compendium of Material Composition Data for Radiation Transport Modeling", PNNL-15870 Rev. 1, 2011.
mat_data["Water"] = {
    "nucvec": {10000000: 11.1894, 80000000: 88.8106},
    "density": 1.0,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["SiC"] = {
    "nucvec": {60000000: 29.9547, 140000000: 70.0453},
    "density": 3.21,
    "citation": "pnnl-15870rev1",
}

# note SS-316L(N)-IG and EUROFER composition (but not density) in
# reference: GilbertNucFus_2017
# M. Gilbert et al., Nucl. Fusion 57 (2017) 046015
#    https://doi.org/10.1088/1741-4326/aa5bd7
#
# more extensive collection of ITER materials composition but not density
# fullreference: GilbertHandbookITERCCFE_2016 M. Gilbert, et al., "Handbook of activation, transmutation, and radiation damage properties of the elements and of ITER materials simulated using FISPACT-II & TENDL-2015; ITER FW armour focus", CCFE-R(16)37, September 2016. https://fispact.ukaea.uk/wp-content/uploads/2016/10/CCFE-R1637.pdf

# reference: GilbertHandbookITERCCFE_2016
# contains 300 wppm B which is important to assess typical He production level
mat_data["SS316LN"] = {
    "nucvec": {
        50000000: 0.030,
        60000000: 0.030,
        70000000: 0.160,
        140000000: 1.0,
        150000000: 0.030,
        160000000: 0.020,
        240000000: 17.250,
        250000000: 2.00,
        260000000: 64.830,
        270000000: 0.100,
        280000000: 12.00,
        410000000: 0.050,
        420000000: 2.5,
    },
    "density": 7.93,
    "citation": "GilbertHandbookITERCCFE_2016",
}

# reference: GilbertHandbookITERCCFE_2016 10 wppm B which is important to assess typical He production level
mat_data["SS316LNIG"] = {
    "nucvec": {
        50000000: 0.001,
        60000000: 0.03,
        70000000: 0.070,
        140000000: 0.50,
        150000000: 0.025,
        160000000: 0.010,
        220000000: 0.10,
        240000000: 17.50,
        250000000: 1.80,
        260000000: 64.844,
        270000000: 0.05,
        280000000: 12.25,
        290000000: 0.30,
        410000000: 0.010,
        420000000: 2.5,
        730000000: 0.01,
    },
    "density": 7.93,
    "citation": "GilbertHandbookITERCCFE_2016",
}

# reference: pnnl-15870rev1
# added 10 wppm B which is important to assess typical He production level
mat_data["SS316L"] = {
    "nucvec": {
        50000000: 0.001,
        60000000: 0.03,
        140000000: 1.0,
        150000000: 0.045,
        160000000: 0.03,
        240000000: 17,
        250000000: 2,
        260000000: 65.394,
        280000000: 12,
        420000000: 2.5,
    },
    "density": 8.00,
    "citation": "pnnl-15870rev1",
}

# reference: FESS-FNSF very similar to GFFpolyimide from ARIES
mat_data["Eins"] = {
    "nucvec": {
        10000000: 1.96,
        60000000: 24.12,
        70000000: 1.46,
        80000000: 40.19,
        120000000: 3.92,
        130000000: 8.6,
        140000000: 19.75,
    },
    "density": 1.8,
    "citation": "FESS-FNSF and ARIES GFFpolyimide",
}

# fullreference: BohmFusSciTec_2019 https://doi.org/10.1080/15361055.2019.1600930
# fullreference: MartelliFusEngDes_2019 https://doi.org/10.1016/j.fusengdes.2018.11.028
mat_data["Pb157Li90"] = {
    "nucvec": {30060000: 0.4905, 30070000: 0.0545, 820000000: 99.455},
    "density": 9.32,  # not sure of Temperature
    "molecular_mass": 175.6273,
    "citation": "BohmFusSciTec_2019",
}


# fullreference: ElGuebalyARIESCSFTI_2006 L. El-Guebaly, "Final Radial Build and Composition for LiPb/FS/He System", Sep. 2006. https://fti.neep.wisc.edu/fti.neep.wisc.edu/aries/BUILD-CS/build092606.pdf
# fullreference: HeizenroederComments2005 P. Heizenroeder and R. Reed "Comments on Selection of U.S. ITER CS Coil Jacket Material", Sep. 12, 2005
mat_data["JK2LBSteel"] = {
    "nucvec": {
        50000000: 0.002,
        60000000: 0.02,
        70000000: 0.2,
        140000000: 0.3,
        150000000: 0.004,
        160000000: 0.004,
        240000000: 13,
        250000000: 21,
        260000000: 55.47,
        280000000: 9,
        420000000: 1,
    },
    "density": 8.0,
    "citation": "ElGuebalyARIESCSFTI_2006",
}

# reference: FESS-FNSF and ???
mat_data["TernaryNb3Sn"] = {
    "nucvec": {410000000: 68.95, 500000000: 30, 220000000: 1.05},
    "density": 8.9,
    "citation": "FESS-FNSF and ???",
}

# reference: ITER and CRC Handbook of Chemistry and Physics density at 4 K
# fullreference: CRChandbook64 64th CRC Handbook of Chemistry and Physics page B-117, density at 4 K
mat_data["LHe"] = {
    "nucvec": {20000000: 100},
    "density": 0.149,
    "citation": "CRChandbook64B117",
}

# fullreference: JawadORNL_2005 M. Jawad et al. , "Development of a New Class of Fe-3Cr-W(V) Ferritic Steels for Industrial Process Applications", ORNL/TM-2005/82, 2005. https://doi.org/10.2172/838517
mat_data["Cr3FS"] = {
    "nucvec": {
        60000: 0.1,
        140000: 0.14,
        230000: 0.25,
        240000: 3.0,
        250000: 0.5,
        260000: 93.01,
        740000: 3.0,
    },
    "density": 7.89,
    "citation": "JawadORNL_2005 and ???",
}

# ODS LiPb-corrosion-resistant steel with Present impurities removed
# fullreference: PintDOE_ER_0313_57_2014 B. Pint et al., DEVELOPMENT OF ODS FeCrAl FOR FUSION REACTOR APPLICATIONS, Fusion Reactor Materials Program Semi-annual Report, Dec. 2014, DOE/ER- 0313/57  Section 2.1, https://fmp.ornl.gov/semiannual-progress-reports/fusion-materials-semiannual-progress-report-57.pdf
# reference: KluehJNM_2000 (for some impurities)
# Density = 7.799 g/cm3, as determined for 14YWT alloy, per David Hoelzer
#
mat_data["ODS125Y"] = {
    "nucvec": {
        60000000: 0.0380,
        70000000: 0.0455,
        80000000: 0.8420,
        130000000: 4.8,
        140000000: 0.02,
        160000000: 0.0020,
        220000000: 0.01,
        240000000: 11.4,
        260000000: 82.6025,
        390000000: 0.19,
        740000000: 0.05,
    },
    "density": 7.799,
    "citation": "PintDOE_ER_0313_57_2014 and KluehJNM_2000 ",
}

# reference: pnnl-15870rev1 at T=20C
mat_data["D2O"] = {
    "nucvec": {10020000: 20.1133, 80000000: 79.8867},
    "density": 1.10534,
    "citation": "pnnl-15870rev1",
}

# fullreference: WidodoJoPCS_2018 Journal of Physics Conference Series doi:10.1088/1742-6596/962/1/012039 and KTA Standards 1986
# also reference: pnnl-15870rev1
mat_data["HeNIST"] = {
    "nucvec": {20000000: 100},
    "density": 0.00016647,  # at 20 C (293.15 K), 1 atm (1.01325 bar)
    "citation": "WidodoJoPCS_2018 and pnnl-15870rev1",
}

# high pressure He gas ref.
# reference: WidodoJoPCS_2018 doi:10.1088/1742-6596/962/1/012039 and KTA Standards 1986
mat_data["HeT410P1"] = {
    "nucvec": {20000000: 100},
    "density": 0.00007048,  # at 410 C, 1 bar
    "citation": "WidodoJoPCS_2018",
}

mat_data["HeT410P80"] = {
    "nucvec": {20000000: 100},
    "density": 0.00571698,  # at 410 C, 80 bar
    "citation": "WidodoJoPCS_2018",
}

# air (Dry, Near Sea Level)
# reference: pnnl-15870rev1
mat_data["AirSTP"] = {
    "nucvec": {
        60000000: 0.0124,
        70000000: 75.5268,
        80000000: 23.1781,
        180000000: 1.2827,
    },
    "density": 0.001205,
    "citation": "pnnl-15870rev1",
}

# concrete (Ordinary NBS 04)
# reference: pnnl-15870rev1
mat_data["Concrete"] = {
    "nucvec": {
        10000000: 0.5558,
        80000000: 49.8076,
        110000000: 1.7101,
        120000000: 0.2565,
        130000000: 4.5746,
        140000000: 31.5092,
        160000000: 0.1283,
        190000000: 1.9239,
        200000000: 8.2941,
        260000000: 1.2398,
    },
    "density": 2.35,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["W"] = {
    "nucvec": {740000000: 100.0},
    "density": 19.30,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["Fe"] = {
    "nucvec": {260000000: 100.0},
    "density": 7.874,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["Na"] = {
    "nucvec": {110000000: 100.0},
    "density": 0.971,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1 reactor graphite without boron impurity
mat_data["C"] = {
    "nucvec": {60000000: 1.0},
    "density": 1.7,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["Si"] = {
    "nucvec": {140000000: 1.0},
    "density": 2.33,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["Cu"] = {
    "nucvec": {290000000: 1.0},
    "density": 8.96,
    "citation": "pnnl-15870rev1",
}

# reference:  pnnl-15870rev1
mat_data["Sn"] = {
    "nucvec": {500000000: 1.0},
    "density": 7.31,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["Ta"] = {
    "nucvec": {730000000: 1.0},
    "density": 16.654,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["Pb"] = {
    "nucvec": {820000000: 100.0},
    "density": 11.35,
    "citation": "pnnl-15870rev1",
}

# fullreference: HernandezFusEngDes_2018 F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018 https://doi.org/10.1016/j.fusengdes.2018.09.014
mat_data["Be"] = {
    "nucvec": {40000000: 1.0},
    "density": 1.85,
    "citation": "HernandezFusEngDes_2018",
}

# reference:  HernandezFusEngDes_2018
# F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018
# https://doi.org/10.1016/j.fusengdes.2018.09.014
mat_data["Be12Ti"] = {
    "atom_frac": {40000000: 12, 220000000: 1},
    "density": 2.28,
    "citation": "HernandezFusEngDes_2018",
}

# reference:  HernandezFusEngDes_2018
# F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018
# https://doi.org/10.1016/j.fusengdes.2018.09.014
mat_data["Be12V"] = {
    "atom_frac": {40000000: 12, 230000000: 1},
    "density": 2.39,
    "citation": "HernandezFusEngDes_2018",
}

li6enrichment = 0.60  # weight fraction enrichment of Li-6 desired
li6enrichStr = f"Li{li6enrichment * 100}"
liXweightfraction = Material({"Li6": li6enrichment, "Li7": (1.0 - li6enrichment)})

# Li ceramics
# reference: HernandezFusEngDes_2018 F.A. Hernandez, P. Pereslavtsev, Fusion Engineering and Design vol. 137, 2018 https://doi.org/10.1016/j.fusengdes.2018.09.014
# F.A. Hernandez, et al., Fusion Engineering and Design, Volume 157, 2020, 111614
# https://doi.org/10.1016/j.fusengdes.2020.111614
# ceramic breeders Li4SiO4 and Li2TiO3 at 60 wt. percent Li-6 EU-DEMO
# note manufacturing may result in lower density of 80-90% of theoretical

mat_data["Li4SiO4nat"] = {
    "atom_frac": {30000000: 4, 80000000: 4, 140000000: 1},
    "density": 2.40,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li2TiO3nat"] = {
    "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.43,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li4SiO4" + li6enrichStr] = {
    "atom_frac": {liXweightfraction: 4, 80000000: 4, 140000000: 1},
    "density": 2.40,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li2TiO3" + li6enrichStr] = {
    "atom_frac": {liXweightfraction: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}

# fullreference: SohalINLEXT-10-18297_2013 M. Sohal et al., "Engineering Database of Liquid Salt Thermophysical and Thermochemical Properties", INL/EXT-10-18297, June 2013. https://inldigitallibrary.inl.gov/sites/STI/STI/5698704.pdf
mat_data["FlibeNat"] = {
    "atom_frac": {30000000: 2, 40000000: 1, 90000000: 4},
    "density": 1.94,
    "citation": "SohalINLEXT-10-18297_2013",
}

# reference: SohalINLEXT-10-18297_2013 M. Sohal et al., "Engineering Database of Liquid Salt Thermophysical and Thermochemical Properties", INL/EXT-10-18297, June 2013. https://inldigitallibrary.inl.gov/sites/STI/STI/5698704.pdf
mat_data["Flibe" + li6enrichStr] = {
    "atom_frac": {liXweightfraction: 2, 40000000: 1, 90000000: 4},
    "density": 1.94,
    "citation": "SohalINLEXT-10-18297_2013",
}

# reference:  pnnl-15870rev1 at STP
mat_data["LiNat"] = {
    "nucvec": {30000000: 1.0},
    "density": 0.534,  # at STP
    "citation": "pnnl-15870rev1",
}

# reference: BohmFusSciTec_2019 rho=0.485 g/cm3 at T=500 C
mat_data["LiNatT500"] = {
    "nucvec": {30000000: 1.0},
    "density": 0.485,  # at T=500 C
    "citation": "BohmFusSciTec_2019",
}

# reference:  pnnl-15870rev1
mat_data[li6enrichStr] = {
    "atom_frac": {liXweightfraction: 1},
    "density": 0.534,  # at STP
    "citation": "pnnl-15870rev1",
}

# reference: BohmFusSciTec_2019 rho=0.485 g/cm3 at T=500 C
mat_data[li6enrichStr + "T500"] = {
    "atom_frac": {liXweightfraction: 1},
    "density": 0.485,  # at T=500 C
    "citation": "BohmFusSciTec_2019",
}

# reference: pnnl-15870rev1
mat_data["Mo"] = {
    "nucvec": {420000000: 100.0},
    "density": 10.22,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["Aluminum6061"] = {
    "nucvec": {
        120000000: 1.0,
        130000000: 97.2,
        140000000: 0.6,
        220000000: 0.088,
        240000000: 0.195,
        250000000: 0.088,
        260000000: 0.4090,
        290000000: 0.275,
        300000000: 0.146,
    },
    "density": 2.70,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["OilTexasCrude"] = {
    "nucvec": {
        10000000: 12.3246,
        60000000: 85.2204,
        70000000: 0.7014,
        160000000: 1.7535,
    },
    "density": 0.875,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["EthyleneGlycol"] = {
    "atom_frac": {10000000: 6, 60000000: 2, 80000000: 2},
    "density": 1.114,
    "citation": "pnnl-15870rev1",
}

# reference: pnnl-15870rev1
mat_data["AluminumOxide"] = {
    "atom_frac": {80000000: 3, 130000000: 2},
    "density": 3.97,
    "citation": "pnnl-15870rev1",
}

# fullreference: GrossbeckJNM_1998 M.L. Grossbeck et al.,"Analysis of V-Cr-Ti alloys in terms of activation of impurities", Journal of Nuclear Materials, vol. 258-263, page 1778-1783 1998. https://doi.org/10.1016/S0022-3115(98)00228-1
# fullreference: ARIES_PropertiesArchive http://qedfusion.org/LIB/PROPS/
# fullreference: MetalsHandbook_1979 Metals Handbook, Ninth Edition, Vol. 2: "Properties and SelectionNonferrous Alloys and Pure Metals," ASM, Metals Park OH (1979)
mat_data["V4Cr4Ti"] = {
    "nucvec": {220000000: 4.0, 230000000: 92.0, 240000000: 4.0},
    "density": 6.05,  # room temperature
    "citation": "GrossbeckJNM_1998 and density ARIES_PropertiesArchive and MetalsHandbook_1979",
}

mat_data["ZrH2"] = {
    "atom_frac": {10000000: 2, 400000000: 1},
    "density": 5.61,  # this is at room temperature
    "citation": "pnnl-15870rev1",
}

#
mat_data["Inconel718"] = {
    "nucvec": {
        50000000: 0.0050,
        60000000: 0.0730,
        130000000: 0.5000,
        140000000: 0.3180,
        150000000: 0.0140,
        160000000: 0.0140,
        220000000: 0.9000,
        240000000: 19.0000,
        250000000: 0.3180,
        260000000: 17.0000,
        280000000: 52.5000,
        270000000: 0.9100,
        290000000: 0.2730,
        410000000: 5.1250,
        420000000: 3.0500,
    },
    "density": 8.19,  # room temperature
    "citation": "pnnl-15870rev1",
}

# reference: aries.ucsd.edu/PROPS/ITER/AM01/AM01-1100.html
# fullreference: CRChandbook64 Bulk density of WC: 64th CRC Handbook of Chemistry and Physics, B-152
mat_data["WC"] = {
    "atom_frac": {60000000: 1, 740000000: 1},
    "density": 15.63,
    "citation": "CRChandbook64B152",
}


# --------------------------------------------------------
def main():
    """Main function to create and write Pure Fusion Materials."""
    mat_lib = MaterialLibrary()
    print("\nCreating Pure Fusion Materials...")

    for mat_name, mat_input in mat_data.items():
        if "nucvec" in mat_input:
            mat_lib[mat_name] = make_mat(
                mat_input["nucvec"],
                mat_input["density"],
                mat_input["citation"],
                mat_input.get("molecular_mass"),
                mat_input.get("mass_enrichment"),
            )
        elif "atom_frac" in mat_input:
            mat_lib[mat_name] = make_mat_from_atom(
                mat_input["atom_frac"],
                mat_input["density"],
                mat_input["citation"],
                mat_input.get("mass_enrichment"),
            )
    # remove lib
    try:
        os.remove("PureFusionMaterials_libv1.json")
    except:
        pass

    # write fnsf1d material library
    mat_lib.write_json("PureFusionMaterials_libv1.json")

    print("All done!")


if __name__ == "__main__":
    main()

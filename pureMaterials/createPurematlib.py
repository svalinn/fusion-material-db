#!/usr/bin/env python3

"""
Pure fusion materials based on FESS-FNSF, ARIES, EU-DEMO.
Can be used for mixing homogenized regions.
Generally impurities at <~1e-3 wt. percent (10 wppm) are removed from materials
(except SS-316 steels may contain boron impurity).
"""

import os
import logging
from typing import Dict, Any, Optional

from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary

# Constants
OUTPUT_HDF5 = "PureFusionMaterials_libv1.h5"
OUTPUT_XML = "PureFusionMaterials_libv1.xml"
OUTPUT_JSON = "PureFusionMaterials_libv1.json"

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def update_nucvec(
    nucvec: Dict[int, float], old_key: int, new_values: Dict[int, float]
) -> Dict[int, float]:
    """Update nuclear vector by replacing an old key with new key-value pairs."""
    if old_key in nucvec:
        fract = nucvec.pop(old_key)
        for key, value in new_values.items():
            nucvec[key] = value * fract
    return nucvec


def make_mat(
    nucvec: Dict[int, float],
    density: float,
    citation: str,
    molecular_mass: Optional[float] = None,
    mass_enrichment: Optional[float] = None,
) -> Material:
    """Create a Material object from nuclear vector data."""
    if mass_enrichment is not None:
        li_weight_fraction = Material(
            {"Li6": mass_enrichment, "Li7": 1.0 - mass_enrichment}
        )
        nucvec = update_nucvec(nucvec, 30000000, li_weight_fraction.comp)

    mat = Material(nucvec, density=density, metadata={"citation": citation})
    if molecular_mass:
        mat.molecular_mass = molecular_mass
    return mat.expand_elements()


def update_atom_frac(
    atom_frac: Dict[int, float], old_key: int, new_values: Material
) -> Dict[int, float]:
    """Update atom fraction by replacing an old key with new values."""
    if old_key in atom_frac:
        atom_frac[new_values] = atom_frac.pop(old_key)
    return atom_frac


def make_mat_from_atom(
    atom_frac: Dict[int, float],
    density: float,
    citation: str,
    mass_enrichment: Optional[float] = None,
) -> Material:
    """Create a Material object from atom fraction data."""
    if mass_enrichment is not None:
        li_weight_fraction = Material(
            {"Li6": mass_enrichment, "Li7": 1.0 - mass_enrichment}
        )
        atom_frac = update_atom_frac(atom_frac, 30000000, li_weight_fraction)

    mat = Material()
    mat.from_atom_frac(atom_frac)
    mat.density = density
    mat.metadata["citation"] = citation
    return mat.expand_elements()


li6enrichment = 0.60  # weight fraction enrichment of Li-6 desired
li6enrichStr = f"Li{li6enrichment * 100}"
liXweightfraction = Material({"Li6": li6enrichment, "Li7": (1.0 - li6enrichment)})

# Material data definitions
mat_data: Dict[str, Dict[str, Any]] = {
    "MF82H": {
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
    },
    "HT9": {
        "nucvec": {
            60000000: 0.2,
            230000000: 0.25,
            240000000: 12.0,
            260000000: 85.55,
            280000000: 0.5,
            420000000: 1.0,
            740000000: 0.5,
        },
        "density": 7.8,
        "citation": "KluehJNM_2000 and SmithBCSSANLvol2_1984",
    },
    "EUROFER97": {
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
    },
    "BMF82H": {
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
    },
    "Water": {
        "nucvec": {10000000: 11.1894, 80000000: 88.8106},
        "density": 1.0,
        "citation": "pnnl-15870rev1",
    },
    "SiC": {
        "nucvec": {60000000: 29.9547, 140000000: 70.0453},
        "density": 3.21,
        "citation": "pnnl-15870rev1",
    },
    "SS316LN": {
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
    },
    "SS316LNIG": {
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
    },
    "SS316L": {
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
    },
    "Eins": {
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
    },
    "Pb157Li90": {
        "nucvec": {30060000: 0.4905, 30070000: 0.0545, 820000000: 99.455},
        "density": 9.32,
        "molecular_mass": 175.6273,
        "citation": "BohmFusSciTec_2019",
    },
    "JK2LBSteel": {
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
    },
    "TernaryNb3Sn": {
        "nucvec": {410000000: 68.95, 500000000: 30, 220000000: 1.05},
        "density": 8.9,
        "citation": "FESS-FNSF and ???",
    },
    "LHe": {
        "nucvec": {20000000: 100},
        "density": 0.149,
        "citation": "CRChandbook64B117",
    },
    "Cr3FS": {
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
    },
    "ODS125Y": {
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
        "citation": "PintDOE_ER_0313_57_2014 and KluehJNM_2000",
    },
    "D2O": {
        "nucvec": {10020000: 20.1133, 80000000: 79.8867},
        "density": 1.10534,
        "citation": "pnnl-15870rev1",
    },
    "HeNIST": {
        "nucvec": {20000000: 100},
        "density": 0.00016647,
        "citation": "WidodoJoPCS_2018 and pnnl-15870rev1",
    },
    "HeT410P1": {
        "nucvec": {20000000: 100},
        "density": 0.00007048,
        "citation": "WidodoJoPCS_2018",
    },
    "HeT410P80": {
        "nucvec": {20000000: 100},
        "density": 0.00571698,
        "citation": "WidodoJoPCS_2018",
    },
    "AirSTP": {
        "nucvec": {
            60000000: 0.0124,
            70000000: 75.5268,
            80000000: 23.1781,
            180000000: 1.2827,
        },
        "density": 0.001205,
        "citation": "pnnl-15870rev1",
    },
    "Concrete": {
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
    },
    "W": {
        "nucvec": {740000000: 100.0},
        "density": 19.30,
        "citation": "pnnl-15870rev1",
    },
    "Fe": {
        "nucvec": {260000000: 100.0},
        "density": 7.874,
        "citation": "pnnl-15870rev1",
    },
    "Na": {
        "nucvec": {110000000: 100.0},
        "density": 0.971,
        "citation": "pnnl-15870rev1",
    },
    "C": {
        "nucvec": {60000000: 1.0},
        "density": 1.7,
        "citation": "pnnl-15870rev1",
    },
    "Si": {
        "nucvec": {140000000: 1.0},
        "density": 2.33,
        "citation": "pnnl-15870rev1",
    },
    "Cu": {
        "nucvec": {290000000: 1.0},
        "density": 8.96,
        "citation": "pnnl-15870rev1",
    },
    "Sn": {
        "nucvec": {500000000: 1.0},
        "density": 7.31,
        "citation": "pnnl-15870rev1",
    },
    "Ta": {
        "nucvec": {730000000: 1.0},
        "density": 16.654,
        "citation": "pnnl-15870rev1",
    },
    "Pb": {
        "nucvec": {820000000: 100.0},
        "density": 11.35,
        "citation": "pnnl-15870rev1",
    },
    "Be": {
        "nucvec": {40000000: 1.0},
        "density": 1.85,
        "citation": "HernandezFusEngDes_2018",
    },
    "Be12Ti": {
        "atom_frac": {40000000: 12, 220000000: 1},
        "density": 2.28,
        "citation": "HernandezFusEngDes_2018",
    },
    "Be12V": {
        "atom_frac": {40000000: 12, 230000000: 1},
        "density": 2.39,
        "citation": "HernandezFusEngDes_2018",
    },
    "Li4SiO4nat": {
        "atom_frac": {30000000: 4, 80000000: 4, 140000000: 1},
        "density": 2.40,
        "citation": "HernandezFusEngDes_2018",
    },
    "Li2TiO3nat": {
        "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
        "density": 3.43,
        "citation": "HernandezFusEngDes_2018",
    },
    f"Li4SiO4{li6enrichStr}": {
        "atom_frac": {liXweightfraction: 4, 80000000: 4, 140000000: 1},
        "density": 2.40,
        "citation": "HernandezFusEngDes_2018",
    },
    f"Li2TiO3{li6enrichStr}": {
        "atom_frac": {liXweightfraction: 2, 80000000: 3, 220000000: 1},
        "density": 3.42,
        "citation": "HernandezFusEngDes_2018",
    },
    "FlibeNat": {
        "atom_frac": {30000000: 2, 40000000: 1, 90000000: 4},
        "density": 1.94,
        "citation": "SohalINLEXT-10-18297_2013",
    },
    f"Flibe{li6enrichStr}": {
        "atom_frac": {liXweightfraction: 2, 40000000: 1, 90000000: 4},
        "density": 1.94,
        "citation": "SohalINLEXT-10-18297_2013",
    },
    "LiNat": {
        "nucvec": {30000000: 1.0},
        "density": 0.534,
        "citation": "pnnl-15870rev1",
    },
    "LiNatT500": {
        "nucvec": {30000000: 1.0},
        "density": 0.485,
        "citation": "BohmFusSciTec_2019",
    },
    li6enrichStr: {
        "atom_frac": {liXweightfraction: 1},
        "density": 0.534,
        "citation": "pnnl-15870rev1",
    },
    f"{li6enrichStr}T500": {
        "atom_frac": {liXweightfraction: 1},
        "density": 0.485,
        "citation": "BohmFusSciTec_2019",
    },
    "Mo": {
        "nucvec": {420000000: 100.0},
        "density": 10.22,
        "citation": "pnnl-15870rev1",
    },
    "Aluminum6061": {
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
    },
    "OilTexasCrude": {
        "nucvec": {
            10000000: 12.3246,
            60000000: 85.2204,
            70000000: 0.7014,
            160000000: 1.7535,
        },
        "density": 0.875,
        "citation": "pnnl-15870rev1",
    },
    "EthyleneGlycol": {
        "atom_frac": {10000000: 6, 60000000: 2, 80000000: 2},
        "density": 1.114,
        "citation": "pnnl-15870rev1",
    },
    "AluminumOxide": {
        "atom_frac": {80000000: 3, 130000000: 2},
        "density": 3.97,
        "citation": "pnnl-15870rev1",
    },
    "V4Cr4Ti": {
        "nucvec": {220000000: 4.0, 230000000: 92.0, 240000000: 4.0},
        "density": 6.05,
        "citation": "GrossbeckJNM_1998 and density ARIES_PropertiesArchive and MetalsHandbook_1979",
    },
    "ZrH2": {
        "atom_frac": {10000000: 2, 400000000: 1},
        "density": 5.61,
        "citation": "pnnl-15870rev1",
    },
    "Inconel718": {
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
        "density": 8.19,
        "citation": "pnnl-15870rev1",
    },
    "WC": {
        "atom_frac": {60000000: 1, 740000000: 1},
        "density": 15.63,
        "citation": "CRChandbook64B152",
    },
}


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

    # Remove existing files only if the respective output has a value
    if OUTPUT_HDF5:
        try:
            os.remove(OUTPUT_HDF5)
            logging.info(f"Removed existing file: {OUTPUT_HDF5}")
        except FileNotFoundError:
            logging.warning(f"File not found, skipping removal: {OUTPUT_HDF5}")

    if OUTPUT_XML:
        try:
            os.remove(OUTPUT_XML)
            logging.info(f"Removed existing file: {OUTPUT_XML}")
        except FileNotFoundError:
            logging.warning(f"File not found, skipping removal: {OUTPUT_XML}")

    if OUTPUT_JSON:
        try:
            os.remove(OUTPUT_JSON)
            logging.info(f"Removed existing file: {OUTPUT_JSON}")
        except FileNotFoundError:
            logging.warning(f"File not found, skipping removal: {OUTPUT_JSON}")

    # Write material library only if it has data
    if mat_lib:
        if OUTPUT_HDF5:
            try:
                mat_lib.write_hdf5(OUTPUT_HDF5)
                logging.info(f"Material library successfully written to {OUTPUT_HDF5}.")
            except Exception as e:
                logging.error(f"Failed to write material library to {OUTPUT_HDF5}: {e}")

        if OUTPUT_XML:
            try:
                mat_lib.write_openmc(OUTPUT_XML)
                logging.info(f"Material library successfully written to {OUTPUT_XML}.")
            except Exception as e:
                logging.error(f"Failed to write material library to {OUTPUT_XML}: {e}")

        if OUTPUT_JSON:
            try:
                mat_lib.write_json(OUTPUT_JSON)
                logging.info(f"Material library successfully written to {OUTPUT_JSON}.")
            except Exception as e:
                logging.error(f"Failed to write material library to {OUTPUT_JSON}: {e}")

    logging.info("All done!")


if __name__ == "__main__":
    main()

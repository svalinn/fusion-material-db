#!/usr/bin/env python3
#
# Updated for Python 3
# Script for mixing pure fusion materials based on FESS-FNSF, ARIES, EUDEMO, and other designs.
# Can be used for mixing homogenized regions.

import os
import logging
from typing import Dict, Any
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary

# Constants
OUTPUT_HDF5 = "mixPureFusionMaterials_libv1.h5"
OUTPUT_XML = "mixPureFusionMaterials_libv1.xml"
OUTPUT_JSON = "mixPureFusionMaterials_libv1.json"

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_constituent_citations(materials) -> str:
    return ", ".join(mat.metadata["citation"] for mat in materials)


def mix_by_volume(
    material_library: MaterialLibrary, vol_fracs: Dict[str, float], citation: str
) -> Material:
    """
    Mixes materials by volume, adds list of constituent citations to the metadata.

    Arguments:
        material_library (MaterialLibrary): Library containing constituent materials.
        vol_fracs (Dict[str, float]): Dictionary where the keys are names of materials and values are the volume fraction.
        citation (str): Citation for the mixture.
    """
    mix_dict = {
        material_library[name]: vol_frac for name, vol_frac in vol_fracs.items()
    }
    mix = MultiMaterial(mix_dict)
    mat = mix.mix_by_volume()
    mat.metadata["mixture_citation"] = citation
    mat.metadata["constituent_citation"] = get_constituent_citations(mix_dict.keys())
    return mat


mat_data: Dict[str, Dict[str, Any]] = {
    "FNSFFW": {
        "vol_fracs": {"MF82H": 0.34, "HeT410P80": 0.66},
        "mixture_citation": "DavisFusEngDes_2018",
    },
    "FNSFFWstruct": {
        "vol_fracs": {"MF82H": 1.0},
        "mixture_citation": "DavisFusEngDes_2018",
    },
    "reIron": {
        "vol_fracs": {"Fe": 1.0},
        "mixture_citation": "pnnl-15870rev1",
    },
    "FNSFDCLL": {
        "vol_fracs": {
            "MF82H": 0.06,
            "Pb157Li90": 0.77,
            "HeT410P80": 0.135,
            "SiC": 0.035,
        },
        "mixture_citation": "EliasUWFMD1424_2015 and MadaniUWFDM1423_2015",
    },
    "EUDEMOHCPB": {
        "vol_fracs": {
            "EUROFER97": 0.118,
            "Be": 0.379,
            "Li4SiO4Li60.0": 0.13,
            "HeT410P80": 0.087,
            "HeT410P1": 0.286,
        },
        "mixture_citation": "EadeFusEngDes_2017",
    },
    "EUDEMOHCPBacb": {
        "vol_fracs": {
            "EUROFER97": 0.118,
            "Be12Ti": 0.379,
            "Li4SiO4Li60.0": 0.0845,
            "Li2TiO3Li60.0": 0.0455,
            "HeT410P80": 0.087,
            "HeT410P1": 0.286,
        },
        "mixture_citation": "ZhouEnergies_2023 and ???",
    },
    "Pbli90BZ": {
        "vol_fracs": {"Pb157Li90": 1.00},
        "mixture_citation": "ARIES and MELCOR TMAP",
    },
    "FlibeLi60BZ": {
        "vol_fracs": {"FlibeLi60.0": 1.0},
        "mixture_citation": "SohalINLEXT-10-18297_2013 and density ???",
    },
    "FNSFIBSR": {
        "vol_fracs": {"MF82H": 0.28, "WC": 0.52, "HeT410P80": 0.20},
        "mixture_citation": "ElGuebalyFusSciTec_2017 and Others",
    },
    "FNSFIBSRstruct": {
        "vol_fracs": {"MF82H": 1.0},
        "mixture_citation": "SchnabelNDS2024",
    },
    "FNSFIBSRfill": {
        "vol_fracs": {"MF82H": 0.05, "WC": 0.686, "HeT410P80": 0.264},
        "mixture_citation": "SchnabelNDS2024",
    },
    "FNSFCC": {
        "vol_fracs": {"SS316LNIG": 1.0},
        "mixture_citation": "DavisFusEngDes_2018",
    },
    "FNSFIBWP": {
        "vol_fracs": {
            "JK2LBSteel": 0.29,
            "Cu": 0.43,
            "TernaryNb3Sn": 0.06,
            "Eins": 0.08,
            "LHe": 0.14,
        },
        "mixture_citation": "SchnabelNDS2024",
    },
    "IFMIFDONESspecimenstack": {
        "vol_fracs": {"EUROFER97": 0.75, "Na": 0.25},
        "mixture_citation": "QiuNucMatEnergy_2018",
    },
    "Pb": {
        "vol_fracs": {"Pb": 1.0},
        "mixture_citation": "pnnl-15870rev1",
    },
    "SS316LN": {
        "vol_fracs": {"SS316LN": 1.0},
        "mixture_citation": "GilbertHandbookITERCCFE_2016",
    },
    "Concrete": {
        "vol_fracs": {"Concrete": 1.0},
        "mixture_citation": "pnnl-15870rev1",
    },
}


def main():
    # Load material library
    mat_lib = MaterialLibrary()
    mat_lib.from_json("PureFusionMaterials_libv1.json")

    # Create material library object
    mixmat_lib = MaterialLibrary()
    for mat_name, mat_input in mat_data.items():
        mixmat_lib[mat_name] = mix_by_volume(
            mat_lib, mat_input["vol_fracs"], mat_input["mixture_citation"]
        )

    # Remove existing files
    for filename in [OUTPUT_HDF5, OUTPUT_XML, OUTPUT_JSON]:
        try:
            os.remove(filename)
            logging.info(f"Removed existing file: {filename}")
        except FileNotFoundError:
            logging.warning(f"File not found, skipping removal: {filename}")

    # Write material library
    mixmat_lib.write_hdf5(OUTPUT_HDF5)
    mixmat_lib.write_openmc(OUTPUT_XML)
    mixmat_lib.write_json(OUTPUT_JSON)
    logging.info("Material library successfully written to all formats.")


if __name__ == "__main__":
    main()

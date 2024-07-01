#!/usr/bin/env python3

"""
Pure fusion materials based on FESS-FNSF, ARIES, EU-DEMO.
Can be used for mixing homogenized regions.
Generally impurities at <~1e-3 wt. percent (10 wppm) are removed from materials
(except SS-316 steels may contain boron impurity).
"""

import os
from typing import Dict, Any, Optional

from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary

# Constants
OUTPUT_HDF5 = "PureFusionMaterials_libv1.h5"
OUTPUT_XML = "PureFusionMaterials_libv1.xml"
OUTPUT_JSON = "PureFusionMaterials_libv1.json"

#Logic for when material without lithium is attempting to be enriched
#Comeback to later to see if there is a better option
class MissingLithiumError(Exception):
  pass

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
        if 30000000 not in nucvec:
            raise MissingLithiumError("This material does not contain lithium, cannot define material.")
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
        if 30000000 not in atom_frac:
            raise MissingLithiumError("This material does not contain lithium, cannot define material.")
        li_weight_fraction = Material(
            {"Li6": mass_enrichment, "Li7": 1.0 - mass_enrichment}
        )
        atom_frac = update_atom_frac(atom_frac, 30000000, li_weight_fraction)
    mat = Material()
    mat.from_atom_frac(atom_frac)
    mat.density = density
    mat.metadata["citation"] = citation
    return mat.expand_elements()


# Material data definitions
# Test configurations 
mat_data: Dict[str, Dict[str, Any]] = {

    "Water_mass_enrich": {
        'nucvec' : {10000000: 11.1894, 80000000: 88.8106},
        "density": 1.00,
        "citation": 'pnnl-15870rev1',
        "mass_enrichment": 0.60,
    },
    "Water_atom_enrich": {
        'nucvec' : {10000000: 11.1894, 80000000: 88.8106},
        "density": 1.00,
        "citation": 'pnnl-15870rev1',
        "mass_enrichment": 0.60,
    },
    "Water_mass_enrich_mol": {
        'nucvec' : {10000000: 11.1894, 80000000: 88.8106},
        "density": 1.00,
        "citation": 'pnnl-15870rev1',
        "molecular_mass": 18.01528,
        "mass_enrichment": 0.60,
    },
    "Water_mass_mol": {
        'nucvec' : {10000000: 11.1894, 80000000: 88.8106},
        "density": 1.00,
        "citation": 'pnnl-15870rev1',
        "molecular_mass": 18.01528,
    },
    "Pb157Li_nat": {
        'nucvec' : {30000000: (0.4905+0.0545),820000000: 99.455},
        "density": 9.32,
        "citation": 'pnnl-15870rev1',
        "molecular_mass": 175.6273,
    },
    "Pb157Li90": {
        'nucvec' : {30060000: 0.4905, 30070000: 0.0545,820000000: 99.455},
        "density": 9.32,
        "citation": 'pnnl-15870rev1',
        "molecular_mass": 175.6273,
    },
    "Pb157Li90_nomol": {
        'nucvec' : {30060000: 0.4905, 30070000: 0.0545,820000000: 99.455},
        "density": 9.32,
        "citation": 'pnnl-15870rev1',
    },
    "Pb157Li90_wrong_mol": {
        'nucvec' : {30060000: 0.4905, 30070000: 0.0545,820000000: 99.455},
        "density": 9.32,
        "citation": 'pnnl-15870rev1',
        "molecular_mass": 132
    },
    "Pb157Li60_wrong": {
        'nucvec' : {30060000: 0.4905, 30070000: 0.0545,820000000: 99.455},
        "density": 9.32,
        "citation": 'pnnl-15870rev1',
        "molecular_mass": 175.6273,
        "mass_enrichment": 0.60,
    },
    "Pb157Li60": {
        'nucvec' : {30000000: (0.4905+0.0545),820000000: 99.455},
        "density": 9.32,
        "citation": 'pnnl-15870rev1',
        "molecular_mass": 175.6273,
        "mass_enrichment": 0.60,
    },
    "Li2TiO3_two": {
        "atom_frac": {80000000: 3, 220000000: 1, 30000000: 2.0},
        "density": 3.43,
        "citation": "HernandezFusEngDes_2018",
        "mass_enrichment": 0.60,
    },
    "Li2TiO3_nat": {
        "atom_frac": {80000000: 3, 220000000: 1, 30000000: 2.0},
        "density": 3.43,
        "citation": "HernandezFusEngDes_2018",
        "mass_enrichment": 0.065,
    },
    "Li2TiO3_m20": {
        "nucvec": {80000000: 3, 220000000: 1, 30000000: 2.0},
        "density": 3.43,
        "citation": "HernandezFusEngDes_2018",
        "mass_enrichment": 0.2,
    },
    "Li2TiO3_mass": {
        "nucvec": {30000000: 2, 80000000: 3, 220000000: 1},
        "density": 3.43,
        "citation": "HernandezFusEngDes_2018",
    },
    "Li2TiO3nat": {
        "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
        "density": 3.43,
        "citation": "HernandezFusEngDes_2018",
    },
    "Li4SiO4nat": {
        'atom_frac' : {30000000:4, 80000000:4, 140000000:1},
        "density": 2.40,
        "citation": "HernandezFusEngDes_2018",
    },
    "Li4SiO4_a20": {
        'atom_frac' : {30000000:4, 80000000:4, 140000000:1},
        "density": 2.40,
        "citation": "HernandezFusEngDes_2018",
        "mass_enrichment": 0.2,
    },
    "Li4SiO4_m20": {
        'nucvec' : {30000000:4, 80000000:4, 140000000:1},
        "density": 2.40,
        "citation": "HernandezFusEngDes_2018",
        "mass_enrichment": 0.2,
    },
    "Li4SiO4_m100": {
        'nucvec' : {30000000:4, 80000000:4, 140000000:1},
        "density": 2.40,
        "citation": "HernandezFusEngDes_2018",
        "mass_enrichment": 1.,
    },
    "Li4SiO4_a100": {
        'atom_frac' : {30000000:4, 80000000:4, 140000000:1},
        "density": 2.40,
        "citation": "HernandezFusEngDes_2018",
        "mass_enrichment": 1.,
    },
}


def main():
    """Main function to create and write Pure Fusion Materials."""
    mat_lib = MaterialLibrary()
    print("\nCreating Pure Fusion Materials...")

    for mat_name, mat_input in mat_data.items():
        try:
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
        except MissingLithiumError as e:
            print(f"Error: {e}. Skipping material {mat_name}.")
    # Remove existing files
    for filename in [OUTPUT_HDF5, OUTPUT_XML, OUTPUT_JSON]:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    # Write material library
    mat_lib.write_hdf5(OUTPUT_HDF5)
    mat_lib.write_openmc(OUTPUT_XML)
    mat_lib.write_json(OUTPUT_JSON)
    print("All done!")


if __name__ == "__main__":
    main()

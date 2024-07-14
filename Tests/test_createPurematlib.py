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

# Information
# All materials made using methods contained in the orginal creatPurematlib.py script have "base" in their name for easy comparison


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
    if mass_enrichment is not None:
        for isotope, enrichment_vector in mass_enrichment.items():
            enriched_mat = Material(
                {key: value for key, value in enrichment_vector.items()}
            )
            nucvec = enrich(nucvec, isotope, enriched_mat.comp)
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
    if mass_enrichment is not None:
        for isotope, enrichment_vector in mass_enrichment.items():
            enriched_mat = Material(
                {key: value for key, value in enrichment_vector.items()}
            )
            # print(enriched_mat, "testing")
            atom_frac = enrich(atom_frac, isotope, enriched_mat.to_atom_frac())

    mat = Material()
    mat.from_atom_frac(atom_frac)
    mat.density = density
    mat.metadata["citation"] = citation
    return mat.expand_elements()


li6enrichment = 0.60  # weight fraction enrichment of Li-6 desired
li6enrichStr = f"Li{li6enrichment * 100}"
liXweightfraction = Material({"Li6": li6enrichment, "Li7": (1.0 - li6enrichment)})

# Newly created to help with unit cases that involve multiple elemtents being enriched
OXweightfraction = Material({"O16": 0.6, "O17": 0.2, "O18": 0.2})

mat_data = {}

mat_data["Li2TiO3_mass_single_base_" + li6enrichStr] = {
    "nucvec": {30060000: (2 * 0.6), 30070000: (2 * 0.40), 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li2TiO3_atom_single_base_" + li6enrichStr] = {
    "atom_frac": {liXweightfraction: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li2TiO3_atom_multi_base" + li6enrichStr] = {
    "atom_frac": {liXweightfraction: 2, OXweightfraction: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li2TiO3_mass_multi_base" + li6enrichStr] = {
    "nucvec": {
        30060000: (2 * 0.6),
        30070000: (2 * 0.40),
        80160000: 0.6 * 3,
        80170000: 0.2 * 3,
        80180000: 0.2 * 3,
        220000000: 1,
    },
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li2TiO3_mass_oxygen_base"] = {
    "nucvec": {
        30000000: 2,
        80160000: 0.6 * 3,
        80170000: 0.2 * 3,
        80180000: 0.2 * 3,
        220000000: 1,
    },
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}

mat_data["Li2TiO3_atom_oxygen_base"] = {
    "atom_frac": {30000000: 2, OXweightfraction: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}

"""
# example of liXweightfraction not working with nucvec uncomment to break
mat_data["Li2TiO3_base_mass_broken" + li6enrichStr] = {
    "nucvec": {liXweightfraction: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}
"""
mat_data["Li2TiO3_atom_single"] = {
    "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {30000000: {30060000: 0.6, 30070000: 0.4}},
}

mat_data["Li2TiO3_mass_single"] = {
    "nucvec": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {30000000: {30060000: 0.6, 30070000: 0.4}},
}

mat_data["Li2TiO3_mass_single_mixed_num_letter"] = {
    "nucvec": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"Li": {"Li6": 0.6, "Li7": 0.4}},
}

mat_data["Li2TiO3_atom_single_mixed_num_letter"] = {
    "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"Li": {"Li6": 0.6, "Li7": 0.4}},
}

mat_data["Li2TiO3_atom_sinlge_mixed_letter_number"] = {
    "atom_frac": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {30000000: {30060000: 0.6, 30070000: 0.4}},
}

mat_data["Li2TiO3_mass_single_mixed_letter_number"] = {
    "nucvec": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {30000000: {30060000: 0.6, 30070000: 0.4}},
}

mat_data["Li2TiO3_atom_single_letter"] = {
    "atom_frac": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"Li": {"Li6": 0.6, "Li7": 0.4}},
}

mat_data["Li2TiO3_mass_single_letter"] = {
    "nucvec": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"Li": {"Li6": 0.6, "Li7": 0.4}},
}

mat_data["Li2TiO3_mass_oxygen_single"] = {
    "nucvec": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2}},
}

mat_data["Li2TiO3_mass_oxygen_single_mixed_num_letter"] = {
    "nucvec": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"O": {"O16": 0.6, "O17": 0.2, "O18": 0.2}},
}

mat_data["Li2TiO3_mass_oxygen_single_letter"] = {
    "nucvec": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"O": {"O16": 0.6, "O17": 0.2, "O18": 0.2}},
}

mat_data["Li2TiO3_atom_oxygen_single"] = {
    "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2}},
}

mat_data["Li2TiO3_atom_oxygen_single_mixed_num_letter"] = {
    "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"O": {"O16": 0.6, "O17": 0.2, "O18": 0.2}},
}

mat_data["Li2TiO3_atom_oxygen_single_letter"] = {
    "atom_frac": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {"O": {"O16": 0.6, "O17": 0.2, "O18": 0.2}},
}


mat_data["Li2TiO3_atom_multi_number"] = {
    "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        30000000: {30060000: 0.6, 30070000: 0.4},
        80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
    },
}

mat_data["Li2TiO3_mass_multi_number"] = {
    "nucvec": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        30000000: {30060000: 0.6, 30070000: 0.4},
        80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
    },
}

mat_data["Li2TiO3_atom_multi_mixed_num_letter"] = {
    "atom_frac": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        "Li": {"Li6": 0.6, "Li7": 0.4},
        "O": {"O16": 0.6, "O17": 0.2, "O18": 0.2},
    },
}

mat_data["Li2TiO3_mass_multi_mixed_num_letter"] = {
    "nucvec": {30000000: 2, 80000000: 3, 220000000: 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        "Li": {"Li6": 0.6, "Li7": 0.4},
        "O": {"O16": 0.6, "O17": 0.2, "O18": 0.2},
    },
}

mat_data["Li2TiO3_atom_multi_letter"] = {
    "atom_frac": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        "Li": {"Li6": 0.6, "Li7": 0.4},
        "O": {"O16": 0.6, "O17": 0.2, "O18": 0.2},
    },
}

mat_data["Li2TiO3_mass_multi_letter"] = {
    "nucvec": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        "Li": {"Li6": 0.6, "Li7": 0.4},
        "O": {"O16": 0.6, "O17": 0.2, "O18": 0.2},
    },
}

mat_data["Li2TiO3_atom_multi_mixed_letter_num"] = {
    "atom_frac": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        30000000: {30060000: 0.6, 30070000: 0.4},
        80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
    },
}

mat_data["Li2TiO3_mass_multi_mixed_letter_num"] = {
    "nucvec": {"Li": 2, "O": 3, "Ti": 1},
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
    "mass_enrichment": {
        30000000: {30060000: 0.6, 30070000: 0.4},
        80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
    },
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
        os.remove("create_test.json")
    except:
        pass

    # write fnsf1d material library
    mat_lib.write_json("create_test.json")

    print("All done!")


if __name__ == "__main__":
    main()

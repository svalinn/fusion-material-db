#! /usr/bin/python
#
# -updated for python3 (print) and updated for changes in python modules
#
#
# mixes pure fusion materials based on FESS-FNSF, ARIES, EUDEMO and other
# designs
# -can be used for mixing homogenized regions
#

# Doesn't work currently to enrich elements that are currently enriched
# If this version moves forward I plan to add logic to warn the user when mat input already contains the isotopes to be enriched

import os
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary
from createPurematlib_test import (
    make_mat,
    make_mat_from_atom,
)
from createPurematlib_test import mat_data as pure
from pyne import nucname


def get_consituent_citations(materials):
    citation_list = []
    for mat in materials:
        citation_list.append(mat.metadata["citation"])

    return ", ".join(citation_list)


# Mix Materials by Volume
def mix_by_volume(material_library, vol_fracs, citation, mass_enrichment=None):

    mix_dict = {}

    for name, volume_fraction in vol_fracs.items():
        material = material_library[name]

        if mass_enrichment and name in mass_enrichment:
            # Will update later so things are less explicit, seems easier to read like this

            material = material.collapse_elements({1})

            nucvec = dict(material.to_atom_frac())

            mat_input = pure[name]
    
            if "atom_frac" in mat_input:

                atom_frac = mat_input["atom_frac"]
                mat_atom_input = dict(atom_frac)
                # Which of the two methods is better?
                enriched_material = make_mat_from_atom(
                    atom_frac=mat_atom_input,
                    density=mat_input["density"],
                    citation=mat_input["citation"],
                    mass_enrichment=mass_enrichment[name],
                )

            else:
                nucvec = mat_input["nucvec"]
                mat_mass_input = dict(nucvec)
                enriched_material_params = {
                    "nucvec": mat_mass_input,
                    "density": mat_input["density"],
                    "citation": mat_input["citation"],
                    "mass_enrichment": mass_enrichment[name],
                }

                enriched_material = make_mat(**enriched_material_params)

            mix_dict[enriched_material.expand_elements()] = volume_fraction
        else:
            mix_dict[material.expand_elements()] = volume_fraction
    mix = MultiMaterial(mix_dict)
    mat = mix.mix_by_volume()
    mat.metadata["mixture_citation"] = citation
    mat.metadata["constituent_citation"] = get_consituent_citations(
        list(mix_dict.keys())
    )
    return mat.expand_elements()


mat_data = {}

# Test 1 testing cases where materials have atom_frac
mat_data["EUDEMOHCPBacb"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4Li60.0": 0.0845,
        "Li2TiO3Li60.0": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
}

mat_data["EUDEMOHCPBacb_atom"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4Li60.0": 0.0845,
        "Li2TiO3nat": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3nat": {30000000: {30060000: 0.6, 30070000: 0.4}},
    },
}

mat_data["EUDEMOHCPBacb_atom_multi"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4nat": 0.0845,
        "Li2TiO3nat": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3nat": {30000000: {30060000: 0.6, 30070000: 0.4}},
        "Li4SiO4nat": {30000000: {30060000: 0.6, 30070000: 0.4}},
    },
}

# Test 2 Testing Enrichment of material made with nucvec
mat_data["EUDEMOHCPBacb_base_mass_test"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass60": 0.0845,
        "Li2TiO3mass60": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
}

mat_data["EUDEMOHCPBacb_mass_test"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass60": 0.0845,
        "Li2TiO3mass": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3mass": {30000000: {30060000: 0.6, 30070000: 0.4}},
    },
}

# Test 3 double atom frac enrichment (oxygen and li enriched )

mat_data["EUDEMOHCPBacb_base_atom_multi_double"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4_atom_oxygen": 0.0845,
        "Li2TiO3_atom_oxygen": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
}


mat_data["EUDEMOHCPBacb_atom_multi_double"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4nat": 0.0845,
        "Li2TiO3nat": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3nat": {
            30000000: {30060000: 0.6, 30070000: 0.4},
            80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
        },
        "Li4SiO4nat": {
            30000000: {30060000: 0.6, 30070000: 0.4},
            80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
        },
    },
}

# Test 4 Multiple material double nucvec enrichment (oxygen and li enriched )

mat_data["EUDEMOHCPBacb_base_mass_multi_double"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4_mass_oxygen": 0.0845,
        "Li2TiO3_mass_oxygen": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
}


mat_data["EUDEMOHCPBacb_mass_multi_double"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass": 0.0845,
        "Li2TiO3mass": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3mass": {
            30000000: {30060000: 0.6, 30070000: 0.4},
            80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
        },
        "Li4SiO4mass": {
            30000000: {30060000: 0.6, 30070000: 0.4},
            80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
        },
    },
}

# Test 5 Single material multiple nucvec enrichment (oxygen and li enriched )

mat_data["EUDEMOHCPBacb_base_mass_single_double"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass60": 0.0845,
        "Li2TiO3_mass_oxygen": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
}


mat_data["EUDEMOHCPBacb_mass_single_double"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass60": 0.0845,
        "Li2TiO3mass": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3mass": {
            30000000: {30060000: 0.6, 30070000: 0.4},
            80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
        },
    },
}


# Test 6 Single material multiple nucvec enrichment (oxygen and li enriched ) but letter

mat_data["EUDEMOHCPBacb_mass_single_double_letter"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass60": 0.0845,
        "Li2TiO3mass": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3mass": {
            "Li": {"Li6": 0.6, "Li7": 0.4},
            "O": {"O16": 0.6, "O17": 0.2, "O18": 0.2},
        },  # add logic to protect against double isotope addition in vector
    },
}


mat_data["EUDEMOHCPBacb_mass_single_double_number_letter"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass60": 0.0845,
        "Li2TiO3mass": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3mass": {
            30000000: {"Li6": 0.6, "Li7": 0.4},
            80000000: {"O16": 0.6, "O17": 0.2, "O18": 0.2},
        },
    },
}

mat_data["EUDEMOHCPBacb_mass_single_double_letter_number"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be12Ti": 0.379,
        "Li4SiO4mass60": 0.0845,
        "Li2TiO3mass": 0.0455,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3mass": {
            "Li": {30060000: 0.6, 30070000: 0.4},
            "O": {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
        },
    },
}


########################################################################
def main():
    # remove old mixmat_lib
    try:
        os.remove("testing_mixedPureFusionMaterials_libv1.json")
    except:
        pass

    # Load material library
    mat_lib = MaterialLibrary()
    mat_lib.from_json("testing_PureFusionMaterials_libv1.json")

    # create material library object
    mixmat_lib = MaterialLibrary()
    for mat_name, mat_input in mat_data.items():
        mixmat_lib[mat_name] = mix_by_volume(
            mat_lib,
            mat_input["vol_fracs"],
            mat_input["mixture_citation"],
            mat_input.get("mass_enrichment"),
        )

    # write fnsf material library
    mixmat_lib.write_json("testing_mixedPureFusionMaterials_libv1.json")


if __name__ == "__main__":
    main()

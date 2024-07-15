#! /usr/bin/python
#
# -updated for python3 (print) and updated for changes in python modules
#
#
# mixes pure fusion materials based on FESS-FNSF, ARIES, EUDEMO and other
# designs
# -can be used for mixing homogenized regions
#
#
#
import os
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary
from createPurematlib_test import (
    make_mat,
    make_mat_from_atom,
)
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
            material = material.collapse_elements({69})  # Collapse material elements
            nucvec = dict(material.to_atom_frac())  # Default to atom fraction

            # Check if enrichment type is specified and apply accordingly
            enrichment_info = mass_enrichment[name]
            if enrichment_info["type"] == "mass":
                nucvec = dict(material)
                # Apply enrichment
                enriched_material = make_mat(
                    nucvec=nucvec,
                    density=material.density,
                    citation=material.metadata.get("citation", ""),
                    mass_enrichment=enrichment_info["data"],  # Pass enrichment data
                )
            else:
                enriched_material = make_mat_from_atom(
                    atom_frac=nucvec,
                    density=material.density,
                    citation=material.metadata.get("citation", ""),
                    mass_enrichment=enrichment_info["data"],  # Pass enrichment data
                )
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
        "Li2TiO3nat": {
            "type": "atom",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
            },
        },
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
        "Li2TiO3nat": {
            "type": "atom",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
            },
        },
        "Li4SiO4nat": {
            "type": "atom",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
            },
        },
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
        "Li2TiO3mass": {
            "type": "mass",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
            },
        },
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
            "type": "atom",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
                80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
            },
        },
        "Li4SiO4nat": {
            "type": "atom",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
                80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
            },
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
            "type": "mass",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
                80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
            },
        },
        "Li4SiO4mass": {
            "type": "mass",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
                80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
            },
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
            "type": "mass",
            "data": {
                30000000: {30060000: 0.6, 30070000: 0.4},
                80000000: {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
            },
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
            "type": "mass",
            "data": {
                "Li": {"Li6": 0.6, "Li7": 0.4},
                "O": {"O16": 0.6, "O17": 0.2, "O18": 0.2},
            },
        },
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
            "type": "mass",
            "data": {
                30000000: {"Li6": 0.6, "Li7": 0.4},
                80000000: {"O16": 0.6, "O17": 0.2, "O18": 0.2},
            },
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
            "type": "mass",
            "data": {
                "Li": {30060000: 0.6, 30070000: 0.4},
                "O": {80160000: 0.6, 80170000: 0.2, 80180000: 0.2},
            },
        },
    },
}


########################################################################
def main():
    # remove old mixmat_lib
    try:
        os.remove("test_mix.json")
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
    mixmat_lib.write_json("test_mix.json")


if __name__ == "__main__":
    main()

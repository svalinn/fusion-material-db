import argparse
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary
from material_db_tools import mix_by_volume
import material_db_tools as mdbt
from material_library import (
    mat_data as pure,
)  # this is importing the material dictionaries

mat_lib_test = MaterialLibrary()
# you may need to adjust this path for your setup
mat_lib_test.from_json("material_library.json")


simulation_lib = MaterialLibrary()


################################### Method 3


# Currently how Edgar and I are enriching out materials
def enriched_lithium(enrichment):
    enriched_li = Material({"Li6": enrichment, "Li7": 1 - enrichment})
    return enriched_li


def Li2TiO3Li_mat(enrichment=0.60):
    Li2TiO3Li60 = Material()
    Li2TiO3Li60.from_atom_frac(
        {enriched_lithium(enrichment): 2, 80000000: 3, 220000000: 1}
    )
    Li2TiO3Li60.density = 3.43
    Li2TiO3Li60 = Li2TiO3Li60.expand_elements()
    Li2TiO3Li60.metadata["citation"] = "HernandezFusEngDes_2018"
    return Li2TiO3Li60


def Li4SiO4Li_mat(enrichment=0.60):
    Li2TiO3Li60 = Material()
    Li2TiO3Li60.from_atom_frac(
        {enriched_lithium(enrichment): 4, 80000000: 4, 140000000: 1}
    )
    Li2TiO3Li60.density = 2.40
    Li2TiO3Li60 = Li2TiO3Li60.expand_elements()
    Li2TiO3Li60.metadata["citation"] = "HernandezFusEngDes_2018"
    return Li2TiO3Li60


# I also need to have another version of this function for the pin breeder zone.
# I will if need to either make a version of this for each material I'm testing
# or I will need a universial function that will require me to pass all the arugments in hcpb_pin_bw()
# plus whatever material I'm testing for the case. Currently I'm testing around 8 different materials
# How I make the universal function will depend on how I can import the library or if I can use enrich
def hcpb_pin_bw(
    enrichment=0.6,
    Li4SiO4_frac=0.065,
    Li2TiO3_frac=0.035,
    he_frac=0.482,
    EUROFER97_frac=0.418,
):

    Li4SiO4Li = Li4SiO4Li_mat(enrichment)
    Li2TiO3Li = Li2TiO3Li_mat(enrichment)

    mix = MultiMaterial(
        {
            mat_lib_test["EUROFER97"]: EUROFER97_frac,
            Li4SiO4Li: Li4SiO4_frac,
            mat_lib_test["HeT410P80"]: he_frac,
            Li2TiO3Li: Li2TiO3_frac,
        }
    )
    hcpb_pin_bw = mix.mix_by_volume()
    hcpb_pin_bw.metadata["constituentcitation"] = "HernandezFusEngDes_2018"
    return hcpb_pin_bw


################################### Method 2

# Method if you want to use enrich function without it being called in mix_by_volume or in make_mat_from_atom
# But this version uses the output json file which will give you the same answer as rebuiling the material to the second last decimal
# Earlier you said that you wanted to avoid that method since you don't trust it
enriched_mat = mdbt.Material({30060000: 0.6, 30070000: 0.4})
collapsed = mat_lib_test["Li2TiO3nat"].collapse_elements({3})
atom_frac_enriched = mdbt.enrich(
    collapsed.to_atom_frac(), 30000000, enriched_mat.to_atom_frac()
)

mat_input2 = {
    "atom_frac": atom_frac_enriched,
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}
material2 = mdbt.make_mat_from_atom(**mat_input2)
# From here you can either add it to the input library or call it in def hcpb_pin_bw
# Benefit of adding to input library you can have it included in your output material library like ss 316 currently


################################### Method 3

# You can either use "from material_library import mat_data as pure" or just redefine the material which would be the same as the current method

enriched_mat = mdbt.Material({30060000: 0.6, 30070000: 0.4})
atom_frac_enriched = mdbt.enrich(
    pure["Li2TiO3nat"]["atom_frac"], 30000000, enriched_mat.to_atom_frac()
)
# I would need to call enrich() each time I wanted to enrich a different element
mat_input3 = {
    "atom_frac": atom_frac_enriched,
    "density": 3.42,
    "citation": "HernandezFusEngDes_2018",
}
material3 = mdbt.make_mat_from_atom(**mat_input3)
# From here you can either add it to the input library or call it in def hcpb_pin_bw


################################### Method 4

# In this method make_mat_from_atom can call the enrich function
# I can enrich multiple isotopes at the same time with this method

pure["Li2TiO3nat"]["mass_enrichment"] = {30000000: {30060000: 0.6, 30070000: 0.4}}
# I can enrich multiple isotopes at the same time with this method
material4 = mdbt.make_mat_from_atom(**pure["Li2TiO3nat"])
mat_lib_test["material4_Li2TiO3"] = material4

# Can also be either added to the input library or call it in def hcpb_pin_bw
# Inputting to the library allows for the mix
pure["Li4SiO4nat"]["mass_enrichment"] = {30000000: {30060000: 0.6, 30070000: 0.4}}
mat_lib_test["material4_Li3SiO4"] = mdbt.make_mat_from_atom(**pure["Li4SiO4nat"])

# You can theoretically enrich the material with one line
#mat_lib_test["material4_Li3SiO4"] = mdbt.make_mat_from_atom(**{**pure.setdefault("Li4SiO4nat", {}), "mass_enrichment": {30000000: {30060000: 0.6, 30070000: 0.4}}}})

mixed_materials = {}

mixed_materials["hcpb_enrich_method_4"] = {
    "vol_fracs": {
        "EUROFER97": 0.418,
        "material4_Li3SiO4": 0.065,
        "material4_Li2TiO3": 0.035,
        "HeT410P80": 0.482,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
}

# If added to the input library you can quite easily combine it with Method 5 but not need to call the mass enrichment function

################################### Method 5

# In this method make_mat_from_atom can be called by mix_by_volume, and make_mat_from_atom can call the the enrich function
# Using Method I'm suggesting, one issue is that it requires the mdbt to import the library that has the materials before they have been created
# With this method I can enrich multiple materials and multiple elements in those materials at the same time.
# It also makes it trivial to add other materials and enrich them
# It would be also fairly easy to add some of the other features such as adjusting the density of materials in this format


mixed_materials["hcpb_enrich_method_5"] = {
    "vol_fracs": {
        "EUROFER97": 0.418,
        "Li4SiO4nat": 0.065,
        "Li2TiO3nat": 0.035,
        "HeT410P80": 0.482,
    },
    "mixture_citation": "ZhouEnergies_2023 and ???",
    "mass_enrichment": {
        "Li2TiO3nat": {30000000: {30060000: 0.6, 30070000: 0.4}},
        "Li4SiO4nat": {30000000: {30060000: 0.6, 30070000: 0.4}},
    },
}


# running results
# I looked at using enrich() to enrich mixed materials after they were made.
# But theres a pretty big difference between making a material and multmaterial even with the same input fraction and overall density.
# I didn't spend a ton of time on it but I could get it to work
def main():
    # Need this function for method 1
    simulation_lib["HCPB_Pin_BW"] = hcpb_pin_bw(
        enrichment=0.6,
        Li4SiO4_frac=0.065,
        Li2TiO3_frac=0.035,
        he_frac=0.482,
        EUROFER97_frac=0.418,
    )

    for material, material_def in mixed_materials.items():
        mat = mix_by_volume(
            mat_lib_test,
            material_def["vol_fracs"],
            citation=material_def.get("citation"),
            mass_enrichment=material_def.get("mass_enrichment"),
        )
        simulation_lib[material] = mat

    # Proof that all methods produce the same enriched material

    # Base comparison from json input
    simulation_lib["Li2TiO3Li60.0"] = mat_lib_test["Li2TiO3Li60.0"]
    # Created from methods 2-4
    simulation_lib["material2"] = material2
    simulation_lib["material3"] = material3
    simulation_lib["material4"] = material4

    simulation_lib.write_openmc("materials_example.xml")


if __name__ == "__main__":
    main()

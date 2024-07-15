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
from createPurematlib import (
    make_mat,
    make_mat_from_atom,
    update_nucvec,
    update_atom_frac,
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
    print("meta")
    return mat.expand_elements()


mat_data = {}


# fullreference: DavisFusEngDes_2018
# https://doi.org/10.1016/j.fusengdes.2017.06.008
mat_data["FNSFFW"] = {
    "vol_fracs": {"MF82H": 0.34, "HeT410P80": 0.66},
    "mixture_citation": "DavisFusEngDes_2018",
}

# fullreference: KluehJNM_2000 R.L. Klueh et al. jnm 2000
# DOI:10.1016/S0022-3115(00)00060-X
mat_data["FNSFFWstruct"] = {
    "vol_fracs": {"MF82H": 1.0},
    "mixture_citation": "DavisFusEngDes_2018",
}

# fullreference: pnnl-15870rev1
mat_data["reIron"] = {
    "vol_fracs": {"Fe": 1.0},
    "mixture_citation": "pnnl-15870rev1",
}
#
# blanket materials

# FNSF OB DCLL Blanket (73.7% LiPb (90% Li-6), 14.9% He/void, 7.5% FS, 3.9% SiC)
# fullreference: EliasUWFMD1424_2015
# https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1424.pdf
# FNSF IB DCLL Blanket (80% LiPb (90% Li-6), 12% He/void, 5% FS, 3% SiC)
# fullreference: MadaniUWFDM1423_2015
# https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1423.pdf
# FNSF DCLL approximate average    77%                  13.5%        6%  3.5%
mat_data["FNSFDCLL"] = {
    "vol_fracs": {
        "MF82H": 0.06,
        "Pb157Li90": 0.77,
        "HeT410P80": 0.135,
        "SiC": 0.035,
    },
    "mixture_citation": "EliasUWFMD1424_2015 and MadaniUWFDM1423_2015",
}

# EUDEMO
# fullreference: EadeFusEngDes_2017 T. Eade et al.,
# Fusion Engineering and Design 124 (2017)
# page 1241-1245 http://dx.doi.org/10.1016/j.fusengdes.2017.02.100
# fullreference: GilbertNucFus_2017 M. Gilbert et al.,
# Nucl. Fusion 57 (2017) 046015 https://doi.org/10.1088/1741-4326/aa5bd7
#

mat_data["EUDEMOHCPB"] = {
    "vol_fracs": {
        "EUROFER97": 0.118,
        "Be": 0.379,
        "Li4SiO4Li60.0": 0.13,
        "HeT410P80": 0.087,
        "HeT410P1": 0.286,
    },
    "mixture_citation": "EadeFusEngDes_2017",
}

# fullreference: ZhouEnergies_2023 G. Zhou et al., Energies 2023, 16,
# 5377 https://doi.org/10.3390/en16145377
# note: latest design uses mixed pebbles Li4SiO4+35 mole% Li2TiO3 and Be12Ti blocks
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

# fullreference: BohmFusSciTec_2019
# https://doi.org/10.1080/15361055.2019.1600930
# fullreference: MartelliFusEngDes_2019
# https://doi.org/10.1016/j.fusengdes.2018.11.028
# generic breeder materials
mat_data["Pbli90BZ"] = {
    "vol_fracs": {"Pb157Li90": 1.00},
    "mixture_citation": "ARIES and MELCOR TMAP",
}


# fullreference: SohalINLEXT-10-18297_2013 M. Sohal et al.,
# "Engineering Database of Liquid Salt Thermophysical and Thermochemical
# Properties", INL/EXT-10-18297, June 2013.
# https://inldigitallibrary.inl.gov/sites/STI/STI/5698704.pdf
mat_data["FlibeLi60BZ"] = {
    "vol_fracs": {"FlibeLi60.0": 1.0},
    "mixture_citation": "SohalINLEXT-10-18297_2013 and density ???",
}


# shielding
# fullreference: ElGuebalyFusSciTec_2017
# https://doi.org/10.1080/15361055.2017.1333865
mat_data["FNSFIBSR"] = {
    "vol_fracs": {"MF82H": 0.28, "WC": 0.52, "HeT410P80": 0.20},
    "mixture_citation": "ElGuebalyFusSciTec_2017 and Others",
}


# fullreference: SchnabelNDS_2024 G. Schnabel et al.,
# "FENDL: A Library for Fusion Research and Applications, Nuclear Data Sheets,
# vol. 193, pages 1-78, 2024. https://doi.org/10.1016/j.nds.2024.01.001
mat_data["FNSFIBSRstruct"] = {
    "vol_fracs": {"MF82H": 1.0},
    "mixture_citation": "SchnabelNDS2024",
}

mat_data["FNSFIBSRfill"] = {
    "vol_fracs": {"MF82H": 0.05, "WC": 0.686, "HeT410P80": 0.264},
    "mixture_citation": "SchnabelNDS2024",
}

mat_data["FNSFCC"] = {
    "vol_fracs": {"SS316LNIG": 1.0},
    "mixture_citation": "DavisFusEngDes_2018",
}

mat_data["FNSFIBWP"] = {
    "vol_fracs": {
        "JK2LBSteel": 0.29,
        "Cu": 0.43,
        "TernaryNb3Sn": 0.06,
        "Eins": 0.08,
        "LHe": 0.14,
    },
    "mixture_citation": "SchnabelNDS2024",
}

mat_data["IFMIFDONESspecimenstack"] = {
    "vol_fracs": {"EUROFER97": 0.75, "Na": 0.25},
    "mixture_citation": "QiuNucMatEnergy_2018",
}

mat_data["Pb"] = {
    "vol_fracs": {"Pb": 1.0},
    "mixture_citation": "pnnl-15870rev1",
}

mat_data["SS316LN"] = {
    "vol_fracs": {"SS316LN": 1.0},
    "mixture_citation": "GilbertHandbookITERCCFE_2016",
}

mat_data["Concrete"] = {
    "vol_fracs": {"Concrete": 1.0},
    "mixture_citation": "pnnl-15870rev1",
}


########################################################################
def main():
    #
    # remove old mixmat_lib
    try:
        os.remove("mixedPureFusionMaterials_libv1.json")
    except:
        pass

    # Load material library
    mat_lib = MaterialLibrary()
    mat_lib.from_json("PureFusionMaterials_libv1.json")

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
    mixmat_lib.write_json("mixedPureFusionMats_libv1.json")


if __name__ == "__main__":
    main()

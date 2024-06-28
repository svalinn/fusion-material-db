# THIS RUNS IN THE DOCKER IMAGE
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary


def load_matlib(lib):
    mat_lib = MaterialLibrary()
    mat_lib.from_hdf5(
        lib, datapath="/mat_name"
    )  # don't set datapath,nucpath...will be pyne default values
    return mat_lib


def mix_FWWArmor(material_library):
    # material library is is PureFusionMaterials
    # composition from 2018 Davis https://doi.org/10.1016/j.fusengdes.2017.06.008
    mix = MultiMaterial({material_library["W"]: 1.0})
    FWWArmor_mat = mix.mix_by_volume()
    FWWArmor_mat.density = FWWArmor_mat.density * 0.913
    FWWArmor_mat.metadata["mat_number"] = 1001
    return FWWArmor_mat


def mix_FNSFBW(material_library):
    # material library is PureFusionMaterials
    # composition from Tim's 2024 FENDL paper
    mix = MultiMaterial(
        {material_library["MF82H"]: 0.80, material_library["HeT410P80"]: 0.20}
    )
    FNSFBW_mat = mix.mix_by_volume()
    FNSFBW_mat.metadata["mat_number"] = 1002
    return FNSFBW_mat


def mix_FNSFHeManifolds(material_library):
    # material library is PureFusionMaterials
    # composition from Tim's 2024 FENDL paper
    mix = MultiMaterial(
        {material_library["HeT410P80"]: 0.70, material_library["MF82H"]: 0.30}
    )
    FNSFHeManifolds_mat = mix.mix_by_volume()
    FNSFHeManifolds_mat.metadata["mat_number"] = 1003
    return FNSFHeManifolds_mat


def mix_VVFill(material_library):
    # material library is PureFusionMaterials
    # composition from T1E radial build spreadsheet
    mix = MultiMaterial(
        {material_library["HeT410P80"]: 0.40, material_library["SS316L"]: 0.60}
    )
    VVFill_mat = mix.mix_by_volume()
    VVFill_mat.metadata["mat_number"] = 1004
    return VVFill_mat


def mix_LTS(material_library):
    # material library is PureFusionMaterials
    # composition from T1E radial build spreadsheet
    mix = MultiMaterial(
        {
            material_library["SS316L"]: 0.39,
            material_library["BMF82H"]: 0.29,
            material_library["Water"]: 0.32,
        }
    )
    LTS_mat = mix.mix_by_volume()
    LTS_mat.metadata["mat_number"] = 1005
    return LTS_mat


def mix_coils(material_library):
    # From T1E radial build spreadsheet
    # material library is PureFusionMaterials
    # mix solder
    mix = MultiMaterial(
        {material_library["Pb"]: 0.4, material_library["Sn"]: 0.6}
    )
    solder_mat = mix.mix_by_volume()

    # mix hts_tape
    mix = MultiMaterial(
        {material_library["SS316L"]: 0.5, material_library["Cu"]: 0.5}
    )
    htsTape_mat = mix.mix_by_volume()

    # mix coils
    mix = MultiMaterial(
        {
            material_library["SS316L"]: 0.7435,
            htsTape_mat: 0.0622,
            material_library["Cu"]: 0.0098 + 0.1209,
            solder_mat: 0.0348,
            material_library["HeT410P80"]: 0.0228 + 0.006,
        }
    )
    coil_mat = mix.mix_by_volume()
    coil_mat.metadata["mat_number"] = 1006
    return coil_mat

def Pb157Li90_mat(enrichment) :
    nucvec = {30060000: 0.4905, 30070000: 0.0545,820000000: 99.455}
    Pb157Li90 = Material(nucvec)
    Pb157Li90.density = 9.32 # not sure of Temperature
    Pb157Li90.molecular_mass = 175.6273
    Pb157Li90=Pb157Li90.expand_elements()
    Pb157Li90.metadata["mat_number"] = 1007
    Pb157Li90.metadata['citation']='BohmFusSciTec_2019'
    return Pb157Li90

def mix_FNSFDCLL(material_library):
    mix = MultiMaterial(
        {
            material_library["MF82H"]: 0.06,
            material_library["Pb157Li90"]: 0.77,
            material_library["HeT410P80"]: 0.135,
            material_library["SiC"]: 0.035,
        }
    )
    FNSFDCLL_mat = mix.mix_by_volume()
    FNSFDCLL_mat.metadata["mat_number"] = 220
    FNSFDCLL_mat.metadata["mixturecitation"] = (
        "EliasUWFMD1424_2015 and MadaniUWFDM1423_2015"
    )
    constituentCitationList = [
        str(material_library["MF82H"].metadata["citation"]),
        str(material_library["Pb157Li90"].metadata["citation"]),
        str(material_library["HeT410P80"].metadata["citation"]),
        str(material_library["SiC"].metadata["citation"]),
    ]
    constituentCitation = " ".join(constituentCitationList)
    FNSFDCLL_mat.metadata["constituentcitation"] = constituentCitation
    print(
        "FNSFDCLL_mat  ",
        FNSFDCLL_mat.metadata["mat_number"],
        FNSFDCLL_mat.density,
    )
    print("   Constituent Citations: ", constituentCitation)
    FNSFDCLL_mat = FNSFDCLL_mat.expand_elements()
    return FNSFDCLL_mat


def mix_FNSFIBSR(material_library):
    mix = MultiMaterial(
        {
            material_library["MF82H"]: 0.28,
            material_library["WC"]: 0.52,
            material_library["HeT410P80"]: 0.20,
        }
    )
    FNSFIBSR_mat = mix.mix_by_volume()
    FNSFIBSR_mat.metadata["mat_number"] = 2242
    FNSFIBSR_mat.metadata["mixturecitation"] = (
        "ElGuebalyFusSciTec_2017 and Others"
    )
    print(
        "FNSFIBSR_mat  ",
        FNSFIBSR_mat.metadata["mat_number"],
        FNSFIBSR_mat.density,
    )
    FNSFIBSR_mat = FNSFIBSR_mat.expand_elements()
    return FNSFIBSR_mat


def mix_FW(material_library):
    # Pure lib
    # from spreadsheet (andy davis)
    mix = MultiMaterial(
        {material_library["MF82H"]: 0.34, material_library["HeT410P80"]: 0.66}
    )
    FW_mat = mix.mix_by_volume()
    FW_mat.metadata["mat_number"] = 1008
    return FW_mat


def main():

    # Load Tim's material libraries
    # ACTUALLY Pyne doesn't seem to like having two libraries loaded
    # at the same time, so I just copied some functions in here. In the
    # future if the materials libraries are included in the repo
    # I could just import the functions
    libPath = "PureFusionMaterials_libv1.h5"
    pureLib = load_matlib(libPath)
    simulationLib = MaterialLibrary()

    # Extract materials from libraries
    FWWArmor = mix_FWWArmor(pureLib)
    FNSFDCLL = mix_FNSFDCLL(pureLib)
    FNSFBW = mix_FNSFBW(pureLib)
    FNSFHeManifolds = mix_FNSFHeManifolds(pureLib)
    FNSFIBSR = mix_FNSFIBSR(pureLib)
    SS316L = pureLib["SS316L"]  # front and back plats of VV
    AirSTP = pureLib["AirSTP"]
    AirSTP.metadata["mat_number"] = 10098
    VVFill = mix_VVFill(pureLib)
    LTS = mix_LTS(pureLib)
    coils = mix_coils(pureLib)
    FW = mix_FW(pureLib)

    # create new material library
    simulationLib["AirSTP"] = AirSTP
    simulationLib["FWWArmor"] = FWWArmor
    simulationLib["FW"] = FW
    simulationLib["FNSFHeManifolds"] = FNSFHeManifolds
    simulationLib["VVFill"] = VVFill
    simulationLib["LTS"] = LTS
    simulationLib["coils"] = coils
    simulationLib["FNSFBW"] = FNSFBW
    simulationLib["FNSFDCLL"] = FNSFDCLL
    simulationLib["FNSFIBSR"] = FNSFIBSR
    simulationLib["SS316L"] = SS316L  # VV front and back plate
    simulationLib.write_openmc("materials.xml")


if __name__ == "__main__":
    main()

# THIS RUNS IN THE DOCKER IMAGE
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary


def load_matlib(lib):
    mat_lib = MaterialLibrary()
    mat_lib.from_hdf5(lib, datapath="/mat_name")
    return mat_lib


def mix_FWWArmor(material_library):
    # material library is is PureFusionMaterials
    # composition from 2018 Davis https://doi.org/10.1016/j.fusengdes.2017.06.008
    mix = MultiMaterial({material_library["W"]: 1.0})
    FWWArmor_mat = mix.mix_by_volume()
    FWWArmor_mat.density = FWWArmor_mat.density * 0.913
    FWWArmor_mat.metadata["mat_number"] = 1001
    return FWWArmor_mat


def mix_PinBW(material_library):
    # material library is is PureFusionMaterials
    # Based on Pin HCPB design from Zhou 2023 paper calculated using Pin Specs spreadsheet
    mix = MultiMaterial(
        {
            material_library["Li4SiO4Li60"]: 0.065,
            material_library["Li2TiO3Li60"]: 0.035,
            material_library["EUROFER97"]: 0.418,
            material_library["HeT410P80"]: 0.482,
        }
    )
    BW_mat = mix.mix_by_volume()
    BW_mat.metadata["mat_number"] = 1022
    return BW_mat


def mix_HeManifolds(material_library):
    # material library is is PureFusionMaterials
    # composition homoegenized based on 50 cm breeder to 35 cm manifold. Manifolds have 5cm Eurofer97 front and back plate with helium inbetween. Estiamted from Zhou 2023 manifolds
    mix = MultiMaterial(
        {material_library["HeT410P80"]: 0.714, material_library["EUROFER97"]: 0.286}
    )
    HeManifolds_mat = mix.mix_by_volume()
    HeManifolds_mat.metadata["mat_number"] = 1003
    return HeManifolds_mat


def mix_Manifolds(material_library):
    # material library is PureFusionMaterials
    # composition homoegenized based on 50 cm breeder to 20 cm manifold. Manifolds have 5cm Eurofer97 front and back plate with helium inbetween.
    mix = MultiMaterial(
        {material_library["HeT410P80"]: 0.5, material_library["EUROFER97"]: 0.5}
    )
    Manifolds_mat = mix.mix_by_volume()
    Manifolds_mat.metadata["mat_number"] = 100352
    return Manifolds_mat


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
    mix = MultiMaterial({material_library["Pb"]: 0.4, material_library["Sn"]: 0.6})
    solder_mat = mix.mix_by_volume()

    # mix hts_tape
    mix = MultiMaterial({material_library["SS316L"]: 0.5, material_library["Cu"]: 0.5})
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


def mix_FNSFIBSR(material_library):
    mix = MultiMaterial(
        {
            material_library["MF82H"]: 0.28,
            material_library["WC"]: 0.52,
            material_library["HeT410P80"]: 0.20,
        }
    )
    FNSFIBSR_mat = mix.mix_by_volume()
    FNSFIBSR_mat.metadata["mat_number"] = 102
    #FNSFIBSR_mat.metadata["mixturecitation"] = "ElGuebalyFusSciTec_2017 and Others"
    print("FNSFIBSR_mat  ", FNSFIBSR_mat.metadata["mat_number"], FNSFIBSR_mat.density)
    FNSFIBSR_mat = FNSFIBSR_mat.expand_elements()
    return FNSFIBSR_mat


def mix_FW(material_library):
    # Pure lib
    # from spreadsheet (andy davis)
    mix = MultiMaterial(
        {material_library["MF82H"]: 0.34, material_library["HeT410P80"]: 0.66}
    )
    FW_mat = mix.mix_by_volume()
    FW_mat.metadata["mat_number"] = 1007
    return FW_mat


def mix_Pin(material_library):
    # Material library is PureFusionMaterials
    # Base Pin HCPB design from Zhou 2023 paper calculated using Pin Specs spreadsheet
    mix = MultiMaterial(
        {
            material_library["Li4SiO4Li60"]: 0.065,
            material_library["Li2TiO3Li60"]: 0.035,
            material_library["Be12Ti"]: 0.613,
            material_library["HeT410P80"]: 0.142,
            material_library["EUROFER97"]: 0.145,
        }
    )
    Pin_mat = mix.mix_by_volume()
    Pin_mat.metadata["mat_number"] = 1009
    print("Pin_mat  ", Pin_mat.metadata["mat_number"], Pin_mat.density)
    return Pin_mat


def main():

    libPath = "PureFusionMaterials_libv1.h5"
    pureLib = load_matlib(libPath)
    simulationLib = MaterialLibrary()

    AirSTP = pureLib["AirSTP"]


    simulationLib["AirSTP"] = AirSTP

    
    simulationLib.write_openmc("materials.xml")


if __name__ == "__main__":
    main()

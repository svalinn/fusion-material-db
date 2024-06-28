from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary


def load_matlib():
    mat_lib=MaterialLibrary()
    mat_lib.from_hdf5("PureFusionMaterials_libv1.h5","HT9") # don't set datapath,nucpath...will be pyne default values
    return mat_lib

print(load_matlib)

def load_matlib(lib):
    mat_lib = MaterialLibrary()
    mat_lib.from_hdf5(
        lib, datapath="/mat_name"
    )  # don't set datapath,nucpath...will be pyne default values
    return mat_lib
libPath = "PureFusionMaterials_libv1.h5"
pureLib = load_matlib(libPath)
print(load_matlib)

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
HCPB = mix_Pin(pureLib)
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary

def make_mat(nucvec, density, citation, molecular_mass = None):
    mat = Material(nucvec, density = density, metadata = {'citation' : citation})
    if molecular_mass:
        mat.molecular_mass = molecular_mass
    return mat.expand_elements()

def make_mat_from_atom(atom_frac, density, citation):
    mat = Material()
    mat.from_atom_frac(atom_frac)
    mat.density = density
    mat.metadata['citation'] = citation
    return mat.expand_elements()


def get_consituent_citations(materials):
    citation_str = ""
    for mat in materials:
        citation_str = " ".join([citation_str, mat.metadata["citation"]])
    return citation_str


# Mix Materials by Volume
def mix_by_volume(material_library, vol_fracs, citation):
    """
    Mixes materials by volume, adds list of constituent citations to the
    metadata

    Arguments:
        material_library (PyNE material library): library containing constituent
            materials.
        vol_fracs (dict): dictionary where the keys are names of materials (str)
            and values are the volume fraction (float)
        citation (str): citation for the mixture
    """
    mix_dict = {}

    for name, volume_fraction in vol_fracs.items():
        mix_dict[material_library[name]] = volume_fraction

    mix = MultiMaterial(mix_dict)
    mat = mix.mix_by_volume()
    mat.metadata["mixture_citation"] = citation
    mat.metadata["constituent_citation"] = get_consituent_citations(
        list(mix_dict.keys())
    )
    return mat


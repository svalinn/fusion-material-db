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


def get_constituent_citations(materials):
    """
    Retrieve citations from a list of materials.

    Arguments:
        materials (list): A list of Material objects.
    Returns:
        citation (str): A comma-separated string of citations.
    """
    citation_list = []
    for mat in materials:
        citation_list.append(mat.metadata["citation"])
    return ", ".join(citation_list)


# Mix Materials by Volume
def mix_by_volume(material_library, vol_fracs, citation, density_factor=1):
    """
    Mixes materials by volume, adds list of constituent citations to the
    metadata

    Arguments:
        material_library (PyNE material library): library containing constituent
            materials.
        vol_fracs (dict): dictionary where the keys are names of materials (str)
            and values are the volume fraction (float)
        citation (str): citation for the mixture
        density_factor (float): Value by which to scale the volume of the
            mixed material. Defaults to 1.
    """

    mix_dict = {}

    for name, volume_fraction in vol_fracs.items():
        mix_dict[material_library[name]] = volume_fraction

    mix = MultiMaterial(mix_dict)
    mat = mix.mix_by_volume()
    mat.density *= density_factor
    mat.metadata["mixture_citation"] = citation
    mat.metadata["constituent_citation"] = get_constituent_citations(
        list(mix_dict.keys())
    )
    return mat


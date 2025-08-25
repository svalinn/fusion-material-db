from typing import Dict, Union, Optional
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary
from pyne import nucname
from decimal import Decimal, getcontext

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
    mat.metadata["constituent_citation"] = get_consituent_citations(
        list(mix_dict.keys())
    )
    return mat


def enrich(
    material_composition: Dict[Union[int, str], float],
    element_to_enrich: Union[int, str],
    isotope_enrichments: Dict[Union[int, str], float],
) -> Dict[int, float]:
    """
    Enrich a specific element in a material composition by replacing it with its isotopes.

    Args:
        material_composition (Dict[Union[int, str], float]): The original material composition.
            Keys can be nuclide IDs (int) or element symbols (str), and values are their fractions (float).
        element_to_enrich (Union[int, str]): The ID or symbol of the element to be enriched.
        isotope_enrichments (Dict[Union[int, str], float]): The isotopic composition for element_to_enrich.
            Keys can be isotope IDs (int) or isotope symbols (str), and values are their enrichment fractions (float).

    Returns:
        Dict[int, float]: The updated material composition with the enriched element.
            Keys are nuclide IDs (int) and values are their fractions (float).
    """
    # Convert all keys to PyNE nuclide IDs
    material_composition = {
        nucname.id(k): Decimal(str(v)) for k, v in material_composition.items()
    }
    isotope_enrichments = {
        nucname.id(k): Decimal(str(v)) for k, v in isotope_enrichments.items()
    }
    element_to_enrich_id = nucname.id(element_to_enrich)

    if element_to_enrich_id in material_composition:
        fract = material_composition.pop(element_to_enrich_id)
        for nuclide, enrich_frac in isotope_enrichments.items():
            material_composition[nuclide] = enrich_frac * fract

    # Convert back to float for consistency with the original function signature
    return {k: float(v) for k, v in material_composition.items()}
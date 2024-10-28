from typing import Dict, Union, Optional
from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary
from pyne import nucname
from decimal import Decimal, getcontext


def make_mat(
    nucvec: Dict[int, float],
    density: float,
    citation: str,
    molecular_mass: Optional[float] = None,
    mass_enrichment: Optional[Dict[int, Dict[int, float]]] = None,
) -> Material:
    """
    Create a Material object from nuclear vector data.

    Args:
        nucvec (Dict[int, float]): The nuclear mass composition vector, with keys as nuclide IDs (zas)
            or the pyne specified element name and values as their fractions (float).
        density (float): The density of the material.
        citation (str): A citation or reference for the material data.
        molecular_mass (Optional[float]): The molecular mass of the material, if applicable.
        mass_enrichment (Optional[Dict[int, Dict[int, float]]]): A dictionary containing the
            enrichment information for elements, where keys are element IDs (int) and values are
            dictionaries with nuclide IDs (int) as keys and enrichment fractions (float) as values.

    Returns:
        Material: The created Material object with the specified properties, based on mass fractions.
    """
    if mass_enrichment:
        for element, enrichment_vector in mass_enrichment.items():
            enriched_mat = Material(enrichment_vector)
            nucvec = enrich(nucvec, element, enriched_mat.comp)
    mat = Material(nucvec, density=density, metadata={"citation": citation})
    if molecular_mass:
        mat.molecular_mass = molecular_mass
    return mat.expand_elements()


def make_mat_from_atom(
    atom_frac: Dict[Union[int, str], float],
    density: float,
    citation: str,
    mass_enrichment: Optional[Dict[int, Dict[int, float]]] = None,
) -> Material:
    """
    Create a Material object from atom fraction data.

    Args:
        atom_frac (Dict[Union[int, str], float]): The atomic fraction composition, with keys as
            nuclide IDs (zas) or the pyne specified element name and values as their fractions (float).
        density (float): The density of the material.
        citation (str): A citation or reference for the material data.
        mass_enrichment (Optional[Dict[int, Dict[int, float]]]): A dictionary containing the
            enrichment information for elements, where keys are element IDs (int) and values are
            dictionaries with nuclide IDs (int) as keys and enrichment fractions (float) as values.

    Returns:
        Material: The created Material object with the specified properties, based on atomic fractions.
    """
    if mass_enrichment:
        for element, enrichment_vector in mass_enrichment.items():
            enriched_mat = Material(enrichment_vector)
            atom_frac = enrich(atom_frac, element, enriched_mat.to_atom_frac())

    mat = Material()
    mat.from_atom_frac(atom_frac)
    mat.density = density
    mat.metadata["citation"] = citation
    return mat.expand_elements()


def get_consituent_citations(materials):
    """
    Retrieve citations from a list of materials.

    Args:
        materials (list): A list of Material objects.

    Returns:
        str: A comma-separated string of citations.
    """
    citation_list = []
    for mat in materials:
        citation_list.append(mat.metadata["citation"])

    return ", ".join(citation_list)


# Mix Materials by Volume
def mix_by_volume(material_library, vol_fracs, citation, mass_enrichment=None):
    from material_library import mat_data as pure
    
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


def enrichment(
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
    element_to_enrich_id = nucname.id(element_to_enrich)
    isotope_enrichments = {
        nucname.id(k): Decimal(str(v)) for k, v in isotope_enrichments.items()
    }

    new_composition = {}

    for nuclide, fraction in material_composition.items():
        nuclide_id = nucname.id(nuclide)
        fraction = Decimal(str(fraction))

        if nuclide_id == element_to_enrich_id:
            # Replace with enriched isotopes
            for isotope, enrich_frac in isotope_enrichments.items():
                new_composition[isotope] = fraction * enrich_frac
        else:
            # Keep the original nuclide
            new_composition[nuclide_id] = fraction

    # Convert back to float for consistency with the original function signature
    return {k: float(v) for k, v in new_composition.items()}


def enrichment(
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
    enriched_material_composition = {}
    element_to_enrich_id = nucname.id(element_to_enrich)

    for k, v in material_composition.items():
        nuclide_id = nucname.id(k)
        fract = Decimal(str(v))

        if nuclide_id == element_to_enrich_id:
            for iso_k, iso_v in isotope_enrichments.items():
                isotope_id = nucname.id(iso_k)
                enriched_material_composition[isotope_id] = Decimal(str(iso_v)) * fract
        else:
            enriched_material_composition[nuclide_id] = fract

    # Convert back to float for consistency with the original function signature
    return {k: float(v) for k, v in enriched_material_composition.items()}


def enrichment(
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
        fract = Decimal(material_composition.pop(element_to_enrich_id))
        for nuclide, enrich_frac in isotope_enrichments.items():
            material_composition[nuclide] = Decimal(enrich_frac) * fract

    # return material_composition
    # Convert back to float for consistency with the original function signature
    return {k: float(v) for k, v in material_composition.items()}


"""def enrich(material_composition, element_to_enrich, isotope_enrichments):
    element_to_enrich_id = nucname.id(element_to_enrich)
    for key in list(material_composition.keys()):
        if nucname.id(key) == element_to_enrich_id:
            fract = Decimal(material_composition.pop(key))
            for nuclide, enrich_frac in isotope_enrichments.items():
                material_composition[nuclide] = Decimal(enrich_frac) * fract
    return material_composition"""


def enrichment(
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
    # Convert all isotope enrichment keys to PyNE nuclide IDs
    isotope_enrichments = {
        nucname.id(k): Decimal(str(v)) for k, v in isotope_enrichments.items()
    }
    element_to_enrich_id = nucname.id(element_to_enrich)

    enriched_material_composition = {}

    for k, v in material_composition.items():
        nuclide_id = nucname.id(k)
        if nuclide_id == element_to_enrich_id:
            fract = Decimal(str(v))
            for isotope_id, enrich_frac in isotope_enrichments.items():
                enriched_material_composition[isotope_id] = Decimal(enrich_frac) * fract
        else:
            enriched_material_composition[nuclide_id] = Decimal(str(v))

    # Convert back to float for consistency with the original function signature
    return {k: float(v) for k, v in enriched_material_composition.items()}

def enrichment(
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
    element_to_enrich_id = nucname.id(element_to_enrich)
    isotope_enrichments = {
        nucname.id(k): Decimal(str(v)) for k, v in isotope_enrichments.items()
    }
    
    enriched_material_composition = {}
    
    for nuclide, fraction in material_composition.items():
        nuclide_id = nucname.id(nuclide)
        fraction = Decimal(str(fraction))
        
        if nuclide_id == element_to_enrich_id:
            for isotope, enrich_frac in isotope_enrichments.items():
                enriched_material_composition[isotope] = fraction * enrich_frac
        else:
            enriched_material_composition[nuclide_id] = fraction
    
    return {k: float(v) for k, v in enriched_material_composition.items()}


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

    enriched_material_composition = {}
    element_to_enrich_id = nucname.id(element_to_enrich)

    for k, v in material_composition.items():
        nuclide_id = nucname.id(k)
        fract = Decimal(str(v))

        if nuclide_id == element_to_enrich_id:
            for iso_k, iso_v in isotope_enrichments.items():
                isotope_id = nucname.id(iso_k)
                enriched_material_composition[isotope_id] = Decimal(str(iso_v)) * fract
        else:
            enriched_material_composition[nuclide_id] = fract

    # Convert back to float for consistency with the original function signature

    return {k: float(v) for k, v in enriched_material_composition.items()}

def enrichment(
    material_composition: Dict[int, float],
    element_to_enrich: int,
    isotope_enrichments: Dict[int, float],
) -> Dict[int, float]:
    """
    Enrich a specific element in a material composition by replacing it with its isotopes.
    Args:
        material_composition: The original material composition.
        element_to_enrich: The ID of the element to be enriched.
        isotope_enrichments: The isotopic composition and ID's for element_to_enrich.
    Returns:
        Dict: The updated material composition with the enriched element.
    """
    element_to_enrich_id = nucname.id(element_to_enrich)
    if element_to_enrich_id in list(material_composition.keys()):
        fract = material_composition.pop(element_to_enrich_id)
        for nuclide, enrich_frac in isotope_enrichments.items():
            material_composition[nuclide] = enrich_frac * fract
    return material_composition

def enrichment(
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
    
    enriched_material_composition = {}
    element_to_enrich_id = nucname.id(element_to_enrich)
    
    for k, v in material_composition.items():
        nuclide_id = nucname.id(k)
        fract = float(v)
        
        if nuclide_id == element_to_enrich_id:
            for iso_k, iso_v in isotope_enrichments.items():
                isotope_id = nucname.id(iso_k)
                enriched_material_composition[isotope_id] = float(iso_v) * fract
        else:
            enriched_material_composition[nuclide_id] = fract
    
    return enriched_material_composition
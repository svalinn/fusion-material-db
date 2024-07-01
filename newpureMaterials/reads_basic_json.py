#!/usr/bin/env python3

#!/usr/bin/env python3

"""
Pure fusion materials based on FESS-FNSF, ARIES, EU-DEMO.
Can be used for mixing homogenized regions.
Generally impurities at <~1e-3 wt. percent (10 wppm) are removed from materials
(except SS-316 steels may contain boron impurity).
"""

import os
import json
import logging
from typing import Dict, Any, Optional

from pyne import material
from pyne.material import Material, MultiMaterial
from pyne.material_library import MaterialLibrary

# Constants
OUTPUT_HDF5 = "test_basic_json.h5"
OUTPUT_XML = "test_basic_json.xml"
OUTPUT_JSON = "test_basic_json.json"
INPUT_JSON = "test.json"  # New constant for input JSON file

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def update_nucvec(
    nucvec: Dict[int, float], old_key: int, new_values: Dict[int, float]
) -> Dict[int, float]:
    """Update nuclear vector by replacing an old key with new key-value pairs."""
    if old_key in nucvec:
        fract = nucvec.pop(old_key)
        for key, value in new_values.items():
            nucvec[key] = nucvec.get(key, 0) + value * fract
    return nucvec


def make_mat(
    nucvec: Dict[int, float],
    density: float,
    citation: str,
    molecular_mass: Optional[float] = None,
    mass_enrichment: Optional[float] = None,
) -> Material:
    """Create a Material object from nuclear vector data."""
    if mass_enrichment is not None:
        li_weight_fraction = Material(
            {"Li6": mass_enrichment, "Li7": 1.0 - mass_enrichment}
        )
        nucvec = update_nucvec(nucvec, 30000000, li_weight_fraction.comp)

    mat = Material(nucvec, density=density, metadata={"citation": citation})
    if molecular_mass:
        mat.molecular_mass = molecular_mass
    return mat.expand_elements()


def update_atom_frac(
    atom_frac: Dict[int, float], old_key: int, new_values: Material
) -> Dict[int, float]:
    """Update atom fraction by replacing an old key with new values."""
    if old_key in atom_frac:
        atom_frac[new_values] = atom_frac.pop(old_key)
    return atom_frac


def make_mat_from_atom(
    atom_frac: Dict[int, float],
    density: float,
    citation: str,
    mass_enrichment: Optional[float] = None,
) -> Material:
    """Create a Material object from atom fraction data."""
    if mass_enrichment is not None:
        li_weight_fraction = Material(
            {"Li6": mass_enrichment, "Li7": 1.0 - mass_enrichment}
        )
        atom_frac = update_atom_frac(atom_frac, 30000000, li_weight_fraction)

    mat = Material()
    mat.from_atom_frac(atom_frac)
    mat.density = density
    mat.metadata["citation"] = citation
    return mat.expand_elements()


def read_material_data(filename: str) -> Dict[str, Dict[str, Any]]:
    """Read material data from a JSON file."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        logger.info(f"Successfully read material data from {filename}")
        return data
    except FileNotFoundError:
        logger.error(f"Input file {filename} not found.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {filename}: {str(e)}")
        return {}


def create_material(mat_name: str, mat_input: Dict[str, Any]) -> Material:
    """Create a Material object based on the input data."""
    if "atom_frac" in mat_input:
        return make_mat_from_atom(
            mat_input["atom_frac"],
            mat_input["density"],
            mat_input["citation"],
            mat_input.get("mass_enrichment"),
        )
    else:
        return make_mat(
            mat_input["nucvec"],
            mat_input["density"],
            mat_input["citation"],
            mass_enrichment=mat_input.get("mass_enrichment"),
        )


def main():
    """Main function to create and write Pure Fusion Materials."""
    logger.info("Starting Pure Fusion Materials creation...")

    # Read material data from JSON file
    mat_data = read_material_data(INPUT_JSON)
    if not mat_data:
        logger.error("No material data available. Exiting.")
        return

    mat_lib = MaterialLibrary()

    for mat_name, mat_input in mat_data.items():
        logger.info(f"Processing material: {mat_name}")
        try:
            # Create material and add to library
            mat_lib[mat_name] = create_material(mat_name, mat_input)
        except KeyError as e:
            logger.error(f"Missing key in material {mat_name}: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing material {mat_name}: {str(e)}")

    # Remove existing files
    for filename in [OUTPUT_HDF5, OUTPUT_XML, OUTPUT_JSON]:
        try:
            os.remove(filename)
            logger.info(f"Removed existing file: {filename}")
        except FileNotFoundError:
            logger.info(f"File not found, skipping removal: {filename}")
        except Exception as e:
            logger.error(f"Error removing file {filename}: {str(e)}")

    # Write material library
    try:
        mat_lib.write_hdf5(OUTPUT_HDF5)
        logger.info(f"Written material library to HDF5: {OUTPUT_HDF5}")
        mat_lib.write_openmc(OUTPUT_XML)
        logger.info(f"Written material library to XML: {OUTPUT_XML}")
        mat_lib.write_json(OUTPUT_JSON)
        logger.info(f"Written material library to JSON: {OUTPUT_JSON}")
        logger.info("All done!")
    except Exception as e:
        logger.error(f"Error writing material library: {str(e)}")


if __name__ == "__main__":
    main()

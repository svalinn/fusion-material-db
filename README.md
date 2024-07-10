# Standard Fusion Materials Database

**Purpose:**

This repository provides a canonical set of materials used widely in fusion neutronics
analysis. Defined using the PyNE toolkit, each pure material has an easy to read definition
and an accompanying reference.

Structure:
* material-db-tools: a set of python methods to facilitate the generation of PyNE material objects
* pureMaterials: a script that defines the composition of a set of pure materials with references 
   and uses `material-db-tools`
* examples: a script that shows how to use `material-db-tools` to mix materials
* db-outputs: pure materials defined in different output formats

## Pure Fusion Materials:
  * For transport calculations
## Fusion Materials with Impurities
  * For activation calculations

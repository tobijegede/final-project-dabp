# Designing an Emergency Water Distribution Plan for Allegheny County
## 94-867A: Decision Analytics for Business and Policy
Jen Andre, Tobi Jegede, Callie Lambert

All data and code files are provided in the final-project-dabp folder. Code files use relative addresses and can be executed on other systems without changes.

The structure of the project folder is as follows:
- final-project-dabp
  - code
    - calc_dist_matrix.py: creates the matrix of distances between POD sites and neighborhoods (Census tracts)
    - prep_census_geo.py: collects and processes Census tract ACS data from the Census API and merges Gazetteer coordinates
    - prep_pod_geo.py: processes raw POD data and geocodes coordinates
    - project_implementation.ipynb: model formulation, implementation, and analysis
  - data
    - 01-raw
      - POD Sites.xlsx: raw data containing street address and other descriptive information for candidate POD sites (provided for project)
      - new_pod_sites.xlsx: raw data containing name and street address for three additional candidate POD sites
    - 02-processed
      - census_geo.csv: contains Census tract data collected and processed with prep_census_geo.py
      - distance_matrix.csv: contains distance matrix created by calc_dist_matrix.py
      - pod_costs_budget.xlsx: contains POD cost and total budget parameters for sensitivity analysis (created manually)
      - pod_geo.csv: contains POD data collected and processed with prep_pod_geo.py

To replicate this analysis, code files should be run as follows:
1. Create processed POD and Census tract data: prep_pod_geo.py, prep_census_geo.py
2. Create distance matrix: calc_dist_matrix.py
3. Run model implementation and analysis: project_implementation.ipynb

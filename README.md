# BioSPEC: Open Molecular Spectroscopic Database

[![Validate & Deploy](https://github.com/Milne-Centre/BioSPEC/actions/workflows/deploy.yml/badge.svg)](https://github.com/Milne-Centre/BioSPEC/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/Code_License-MIT-yellow.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data_License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An open, automated database of rotational and vibrational spectroscopic data for astrobiological biosignatures, planetary atmosphere modeling, and astrochemistry.

**Live Database:** [https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/](https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/)

---

## Key Features

* **Interactive Search & Filtering:** Fast in-browser filtering by chemical formula, isotopologue, name, state, and theoretical method via DataTables.
* **Automated Indexing:** Adding a JSON file to the `data/` folder automatically validates the schema, builds `search_index.json`, and deploys the updated web application.
* **Open & Machine-Readable:** Standardized JSON formatting designed for easy programmatic parsing and reproducible research.

---

## Directory Structure

```text
├── index.html            # Web interface (HTML/JS/DataTables)
├── build_index.py        # Python script that validates & compiles data/*.json
├── search_index.json     # Compiled database index (generated automatically)
├── data/                 # Individual molecular JSON records
│   ├── H2O.json
│   └── ...
└── .github/
    └── workflows/
        └── deploy.yml    # Automated build & deployment pipeline

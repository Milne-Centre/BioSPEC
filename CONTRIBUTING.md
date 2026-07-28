# Contributing to BioSPEC

Thank you for contributing spectroscopic data to BioSPEC! By adding molecular records to this database, you help build an open resource for planetary atmospheric modeling, astrochemistry, and biosignature detection.

To ensure all data remains clean, searchable, and machine-readable, every contribution must follow the guidelines below.

--------------------------------------------------------------------------------

### 1. File Naming and Location

* Directory: All individual molecule records MUST be placed in the "data/" folder.
* Filename: Name your file using the chemical formula (e.g., "data/CH4.json", "data/H2O.json", or "data/HOBr.json").
* Uniqueness: Check the "data/" folder before starting to ensure no one else has already added or claimed your assigned molecule.

--------------------------------------------------------------------------------

### 2. JSON Format and Data Schema

Every file must be valid JSON and contain at minimum the "formula" and "source_type" fields.

JSON Template:
```json
{
  "formula": "CH4",
  "source_type": "computation",
  "isotopologue": "12C-1H4",
  "name": "Methane",
  "electronic_state": "X^1A1",
  "label": "B3LYP/cc-pVTZ Anharmonic",
  "reference_doi": "10.1021/acs.jpca.0c00000",
  "computation_metadata": {
    "method": "B3LYP",
    "basis_set": "cc-pVTZ",
    "software": "Gaussian 16"
  },
  "vibrational_modes": [
    {
      "mode_id": "v1",
      "label": "Symmetric stretch",
      "harmonic": 3025.5,
      "anharmonic": 2916.5
    }
  ]
}
```

Important Formatting Rules:

1. Allowed "source_type" Values: Must be either "computation" or "experiment".
2. Numeric Types: Frequencies, constants, and scaling factors must be numbers (e.g., 3025.5), not strings in quotes ("3025.5").
3. No Trailing Commas: Ensure there is no trailing comma after the last item in an array or object.
4. Missing Values: If data for an optional field (e.g., "anharmonic_unc") is unavailable, omit the key or set its value to null.

--------------------------------------------------------------------------------

### 3. How to Submit Your Data

Option A: Via GitHub Web Interface (Easiest)

1. Open the repository on GitHub and navigate into the "data/" folder.
2. Click "Add file" -> "Create new file".
3. Name your file "data/YOUR_MOLECULE.json" (e.g., "data/NH3.json").
4. Paste your JSON content into the editor box.
5. Scroll down to "Commit changes..."
6. Select "Create a new branch for this commit and start a pull request".
7. Click "Propose changes", then click "Create pull request".

Option B: Via Command Line / Git

1. Clone the repository and create a new feature branch:
   git checkout -b add-molecule-nh3

2. Create your .json file inside the "data/" folder.
3. Commit and push your changes:
   git add data/NH3.json
   git commit -m "Add spectroscopic record for NH3"
   git push origin add-molecule-nh3

4. Open a Pull Request (PR) on GitHub against the main branch.

--------------------------------------------------------------------------------

### 4. Automated Validation Checks

Once your Pull Request is submitted, GitHub Actions will automatically run validate_data.py using Pydantic to verify your file.

* Passing Check [PASS]: Your JSON syntax is valid and meets all schema requirements. A reviewer will merge your pull request, triggering the automated index build and site deployment.
* * Failing Check [FAIL]: Validation failed. Click "Details" next to the failed check to inspect the error log (e.g., missing field, incorrect data type, or syntax error). Edit your file on your branch to fix the issue--the validator will re-test automatically upon save! 

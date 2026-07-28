import json
import glob

def build_index():
    data_list = []
    for file in glob.glob("data/*.json"):
        with open(file, 'r') as f:
            entries = json.load(f)
            
            # Ensure it's a list
            if not isinstance(entries, list):
                entries = [entries]
                
            # Loop through each entry in the molecule file
            for entry in entries:
                data_list.append({
                    "label": entry.get("label"),
                    "formula": entry["formula"],
                    "isotopologue": entry["isotopologue"],
                    "name": entry["name"],
                    "electronic_state": entry["electronic_state"],
                    "source_type": entry.get("source_type"),
                    "computation_metadata": entry.get("computation_metadata"),
                    "reference_doi": entry.get("reference_doi"),
                    "vibrational_modes": entry["vibrational_modes"]
                })
                
    with open("search_index.json", "w") as f:
        json.dump(data_list, f, indent=2)
    print("Successfully built search_index.json")

if __name__ == "__main__":
    build_index()


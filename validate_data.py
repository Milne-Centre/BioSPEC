from __future__ import annotations  # <-- Enables forward references globally
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
import json
import glob

from typing import Optional
from pydantic import BaseModel

class MoleculeEntry(BaseModel):
    label: str
    formula: str
    isotopologue: str
    name: str
    electronic_state: str
    source_type: str
    vibrational_modes: list[VibrationalMode]

class RotationalConstants(BaseModel):
    A: float
    A_unc: Optional[float] = None
    A_doi: Optional[str] = None
    B: float
    B_unc: Optional[float] = None
    B_doi: Optional[str] = None
    C: float
    C_unc: Optional[float] = None
    C_doi: Optional[str] = None

class VibrationalMode(BaseModel):
    mode_id: int
    harmonic: Optional[float] = None  # Accepts float or null
    harmonic_unc: Optional[float] = None
    harmonic_doi: Optional[str] = None
    anharmonic: Optional[float] = None  # Accepts float or null
    anharmonic_unc: Optional[float] = None
    anharmonic_doi: Optional[str] = None
    rotational_constants: RotationalConstants
    reference_doi: Optional[str] = None  # Mode-specific DOI fallback

class ComputationMetadata(BaseModel):
    method: str
    basis_set: str
    software: Optional[str] = None
    scaling_factor: Optional[float] = None

class MoleculeEntry(BaseModel):
    label: Optional[str] = None
    formula: str
    isotopologue: str
    name: str
    electronic_state: str
    source_type: str  # "computation" or "experiment"
    
    # Required if source_type == "computation"
    computation_metadata: Optional[ComputationMetadata] = None
    
    # Required if source_type == "experiment"
    reference_doi: Optional[str] = None
    
    vibrational_modes: List[VibrationalMode]

    @model_validator(mode='after')
    def validate_source_requirements(self) -> 'MoleculeEntry':
        if self.source_type == "computation" and not self.computation_metadata:
            raise ValueError("Entries with source_type 'computation' must include 'computation_metadata'.")
        if self.source_type == "experiment" and not self.reference_doi:
            raise ValueError("Entries with source_type 'experiment' must include a 'reference_doi'.")
        return self

def validate_data(directory="data/"):
    files = glob.glob(f"{directory}/*.json")
    validation_failed = False
    
    if not files:
        print(f"⚠️ No JSON files found in directory: {directory}")
        return

    for file in files:
        with open(file, 'r') as f:
            try:
                raw_data = json.load(f)
                
                # Ensure root is a list of entries
                if not isinstance(raw_data, list):
                    raise ValueError("Root JSON structure must be a list of entries ([...]).")
                
                # Validate each entry in the list
                for entry in raw_data:
                    MoleculeEntry(**entry)
                    
                print(f"✅ Validated: {file}")
            except Exception as e:
                validation_failed = True
                print(f"❌ Error in {file}: {e}")
                
    if validation_failed:
        exit(1)

if __name__ == "__main__":
    validate_data()


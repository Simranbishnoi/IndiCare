import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"/"synthea"


def extract_csv(filename):
    """
    Read one Synthea CSV file from data/raw/.
    """

    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {file_path}"
        )

    return pd.read_csv(
        file_path,
        low_memory=False
    )


def extract_patients():
    """
    Extract PATIENTS data.
    """

    patients = extract_csv("patients.csv")

    print(
        f"patients: {len(patients)} rows, "
        f"{len(patients.columns)} columns"
    )

    return patients
def extract_encounters():
    encounters = extract_csv("encounters.csv")
    print(f"encounters: {len(encounters)} rows, {len(encounters.columns)} columns")
    return encounters
def extract_careplans():
    careplans = extract_csv("careplans.csv")
    print(f"careplans: {len(careplans)} rows, {len(careplans.columns)} columns")
    return careplans

if __name__ == "__main__":
    patients = extract_patients()
    encounters = extract_encounters()
    careplans = extract_careplans()

    print("\nPATIENTS columns:")
    print(patients.columns.tolist())

    print("\nENCOUNTERS columns:")
    print(encounters.columns.tolist())

    print("\nCAREPLANS columns:")
    print(careplans.columns.tolist())
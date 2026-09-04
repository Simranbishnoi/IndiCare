import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Raw Synthea data directory
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def extract_csv(filename):
    """
    Read one Synthea CSV file.

    This function only extracts data.
    It does not clean or transform anything.
    """

    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {file_path}"
        )

    return pd.read_csv(file_path)


def extract_all():
    """
    Extract the five clinical datasets
    assigned to Teammate 2.
    """

    conditions = extract_csv("conditions.csv")
    observations = extract_csv("observations.csv")
    medications = extract_csv("medications.csv")
    procedures = extract_csv("procedures.csv")
    allergies = extract_csv("allergies.csv")

    return {
        "conditions": conditions,
        "observations": observations,
        "medications": medications,
        "procedures": procedures,
        "allergies": allergies,
    }


if __name__ == "__main__":

    data = extract_all()

    for name, df in data.items():
        print(
            f"{name}: "
            f"{df.shape[0]} rows, "
            f"{df.shape[1]} columns"
        )
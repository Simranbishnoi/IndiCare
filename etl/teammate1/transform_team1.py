import pandas as pd
from pathlib import Path

from extract_team1 import (
    extract_patients,
    extract_encounters,
    extract_careplans
)

from clean_team1 import (
    clean_patients,
    clean_encounters,
    clean_careplans
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# =========================================================
# PATIENTS TRANSFORMATION
# =========================================================

def transform_patients(df):
    keep_columns = [
        "Id",
        "FIRST",
        "LAST",
        "BIRTHDATE",
        "DEATHDATE",
        "MARITAL",
        "RACE",
        "ETHNICITY",
        "GENDER",
        "COUNTY",
        "FIPS",
        "ZIP",
        "LAT",
        "LON"
    ]

    transformed = df[keep_columns].copy()

    transformed["BIRTHDATE"] = pd.to_datetime(
        transformed["BIRTHDATE"],
        errors="coerce"
    )

    transformed["DEATHDATE"] = pd.to_datetime(
        transformed["DEATHDATE"],
        errors="coerce"
    )

    transformed["FIPS"] = transformed["FIPS"].astype("string")
    transformed["ZIP"] = transformed["ZIP"].astype("string")

    return transformed


# =========================================================
# ENCOUNTERS TRANSFORMATION
# =========================================================

def transform_encounters(df):
    keep_columns = [
        "Id",
        "START",
        "STOP",
        "PATIENT",
        "ORGANIZATION",
        "PROVIDER",
        "PAYER",
        "ENCOUNTERCLASS",
        "CODE",
        "REASONCODE",
        "REASONDESCRIPTION"
    ]

    transformed = df[keep_columns].copy()

    transformed["START"] = pd.to_datetime(
        transformed["START"],
        errors="coerce",
        utc=True
    )

    transformed["STOP"] = pd.to_datetime(
        transformed["STOP"],
        errors="coerce",
        utc=True
    )

    return transformed


# =========================================================
# CAREPLANS TRANSFORMATION
# =========================================================

def transform_careplans(df):
    keep_columns = [
        "Id",
        "START",
        "STOP",
        "PATIENT",
        "ENCOUNTER",
        "CODE",
        "DESCRIPTION",
        "REASONCODE",
        "REASONDESCRIPTION"
    ]

    transformed = df[keep_columns].copy()

    transformed["START"] = pd.to_datetime(
        transformed["START"],
        errors="coerce",
        utc=True
    )

    transformed["STOP"] = pd.to_datetime(
        transformed["STOP"],
        errors="coerce",
        utc=True
    )

    return transformed


# =========================================================
# MAIN ETL EXECUTION
# =========================================================

if __name__ == "__main__":

    # -------------------------
    # PATIENTS
    # -------------------------

    patients = extract_patients()

    cleaned_patients = clean_patients(patients)

    transformed_patients = transform_patients(
        cleaned_patients
    )

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    patients_output = (
        PROCESSED_DIR / "patients_processed.csv"
    )

    transformed_patients.to_csv(
        patients_output,
        index=False
    )

    print("\nPATIENT TRANSFORMATION SUCCESSFUL")
    print("---------------------------------")
    print("Rows:", len(transformed_patients))
    print("Columns:", len(transformed_patients.columns))

    print("\nColumns retained:")
    print(transformed_patients.columns.tolist())

    print("\nData types:")
    print(transformed_patients.dtypes)

    print("\nSaved to:")
    print(patients_output)


    # -------------------------
    # ENCOUNTERS
    # -------------------------

    encounters = extract_encounters()

    cleaned_encounters = clean_encounters(
        encounters
    )

    transformed_encounters = transform_encounters(
        cleaned_encounters
    )

    encounters_output = (
        PROCESSED_DIR / "encounters_processed.csv"
    )

    transformed_encounters.to_csv(
        encounters_output,
        index=False
    )

    print("\nENCOUNTER TRANSFORMATION SUCCESSFUL")
    print("-----------------------------------")
    print("Rows:", len(transformed_encounters))
    print("Columns:", len(transformed_encounters.columns))

    print("\nColumns retained:")
    print(transformed_encounters.columns.tolist())

    print("\nData types:")
    print(transformed_encounters.dtypes)

    print("\nSaved to:")
    print(encounters_output)


    # -------------------------
    # CAREPLANS
    # -------------------------

    careplans = extract_careplans()

    cleaned_careplans = clean_careplans(
        careplans
    )

    transformed_careplans = transform_careplans(
        cleaned_careplans
    )

    careplans_output = (
        PROCESSED_DIR / "careplans_processed.csv"
    )

    transformed_careplans.to_csv(
        careplans_output,
        index=False
    )

    print("\nCAREPLAN TRANSFORMATION SUCCESSFUL")
    print("----------------------------------")
    print("Rows:", len(transformed_careplans))
    print("Columns:", len(transformed_careplans.columns))

    print("\nColumns retained:")
    print(transformed_careplans.columns.tolist())

    print("\nData types:")
    print(transformed_careplans.dtypes)

    print("\nSaved to:")
    print(careplans_output)
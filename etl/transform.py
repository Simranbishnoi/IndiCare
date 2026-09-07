import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Raw data is directly inside data/raw/
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# CONDITIONS
# ---------------------------------------------------------

def transform_conditions(df):
    """
    Transform cleaned CONDITIONS data.

    Synthea column names are kept unchanged.
    """

    transformed = df.copy()

    # Keep required CONDITIONS columns.
    transformed = transformed[
        [
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTER",
            "CODE",
            "DESCRIPTION",
        ]
    ].copy()

    # Convert date columns.
    transformed["START"] = pd.to_datetime(
        transformed["START"],
        errors="coerce"
    )

    transformed["STOP"] = pd.to_datetime(
        transformed["STOP"],
        errors="coerce"
    )

    # Create ConditionCode reference data.
    condition_codes = (
        transformed[
            ["CODE", "DESCRIPTION"]
        ]
        .drop_duplicates()
        .sort_values("CODE")
        .reset_index(drop=True)
    )

    return transformed, condition_codes


# ---------------------------------------------------------
# OBSERVATIONS
# ---------------------------------------------------------

def transform_observations(df):
    """
    Transform cleaned OBSERVATIONS data.

    Synthea column names are kept unchanged.
    """

    transformed = df.copy()

    # Keep required OBSERVATIONS columns.
    transformed = transformed[
        [
            "DATE",
            "PATIENT",
            "ENCOUNTER",
            "CATEGORY",
            "CODE",
            "DESCRIPTION",
            "VALUE",
            "UNITS",
            "TYPE",
        ]
    ].copy()

    # Convert observation date.
    transformed["DATE"] = pd.to_datetime(
        transformed["DATE"],
        errors="coerce"
    )

    # Do NOT arbitrarily change the description for CODE 6299-2.
    # The validation finding is documented, but the final
    # standardized description has not yet been selected.

    # Create ObservationCode reference data.
    observation_codes = (
        transformed[
            ["CODE", "DESCRIPTION"]
        ]
        .drop_duplicates()
        .sort_values("CODE", na_position="last")
        .reset_index(drop=True)
    )

    return transformed, observation_codes


# ---------------------------------------------------------
# MEDICATIONS
# ---------------------------------------------------------

def transform_medications(df):
    """
    Transform cleaned MEDICATIONS data.

    Synthea column names are kept unchanged.
    """

    transformed = df.copy()

    # Keep all source columns belonging to MEDICATIONS.
    transformed = transformed[
        [
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTER",
            "CODE",
            "DESCRIPTION",
            "BASE_COST",
            "PAYER_COVERAGE",
            "DISPENSES",
            "TOTALCOST",
            "REASONCODE",
            "REASONDESCRIPTION",
        ]
    ].copy()

    # Convert medication dates.
    transformed["START"] = pd.to_datetime(
        transformed["START"],
        errors="coerce"
    )

    transformed["STOP"] = pd.to_datetime(
        transformed["STOP"],
        errors="coerce"
    )

    # Create MedicationCode reference data.
    #
    # Multiple descriptions for some medication codes were
    # found during validation. Therefore, we do not silently
    # select or overwrite a description here.
    medication_codes = (
        transformed[
            ["CODE", "DESCRIPTION"]
        ]
        .drop_duplicates()
        .sort_values("CODE")
        .reset_index(drop=True)
    )

    return transformed, medication_codes


# ---------------------------------------------------------
# PROCEDURES
# ---------------------------------------------------------

def transform_procedures(df):
    """
    Transform cleaned PROCEDURES data.

    Synthea column names are kept unchanged.

    Known validation issues are preserved for investigation:
    - one STOP < START record
    - inconsistent DESCRIPTION for CODE 171207006
    """

    transformed = df.copy()

    # Keep required PROCEDURES columns.
    transformed = transformed[
        [
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTER",
            "SYSTEM",
            "CODE",
            "DESCRIPTION",
            "BASE_COST",
            "REASONCODE",
            "REASONDESCRIPTION",
        ]
    ].copy()

    # Convert procedure dates.
    transformed["START"] = pd.to_datetime(
        transformed["START"],
        errors="coerce"
    )

    transformed["STOP"] = pd.to_datetime(
        transformed["STOP"],
        errors="coerce"
    )

    # Create ProcedureCode reference data.
    #
    # The description inconsistency for CODE 171207006 is
    # intentionally not silently corrected.
    procedure_codes = (
        transformed[
            ["CODE", "DESCRIPTION"]
        ]
        .drop_duplicates()
        .sort_values("CODE")
        .reset_index(drop=True)
    )

    return transformed, procedure_codes


# ---------------------------------------------------------
# ALLERGIES
# ---------------------------------------------------------

def transform_allergies(df):
    """
    Transform cleaned ALLERGIES data.

    Synthea column names are kept unchanged.
    """

    transformed = df.copy()

    # Keep required ALLERGIES columns.
    transformed = transformed[
        [
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTER",
            "CODE",
            "SYSTEM",
            "DESCRIPTION",
            "TYPE",
            "CATEGORY",
            "REACTION1",
            "DESCRIPTION1",
            "SEVERITY1",
            "REACTION2",
            "DESCRIPTION2",
            "SEVERITY2",
        ]
    ].copy()

    # Convert allergy dates.
    transformed["START"] = pd.to_datetime(
        transformed["START"],
        errors="coerce"
    )

    transformed["STOP"] = pd.to_datetime(
        transformed["STOP"],
        errors="coerce"
    )

    # Create AllergyCode reference data.
    allergy_codes = (
        transformed[
            ["CODE", "DESCRIPTION"]
        ]
        .drop_duplicates()
        .sort_values("CODE")
        .reset_index(drop=True)
    )

    return transformed, allergy_codes


# ---------------------------------------------------------
# TRANSFORM ALL TABLES
# ---------------------------------------------------------

def transform_all(data):
    """
    Transform all five Teammate 2 datasets.
    """

    conditions, condition_codes = transform_conditions(
        data["conditions"]
    )

    observations, observation_codes = transform_observations(
        data["observations"]
    )

    medications, medication_codes = transform_medications(
        data["medications"]
    )

    procedures, procedure_codes = transform_procedures(
        data["procedures"]
    )

    allergies, allergy_codes = transform_allergies(
        data["allergies"]
    )

    return {
        "conditions": conditions,
        "condition_codes": condition_codes,

        "observations": observations,
        "observation_codes": observation_codes,

        "medications": medications,
        "medication_codes": medication_codes,

        "procedures": procedures,
        "procedure_codes": procedure_codes,

        "allergies": allergies,
        "allergy_codes": allergy_codes,
    }


# ---------------------------------------------------------
# SAVE PROCESSED DATA
# ---------------------------------------------------------

def save_transformed(data):
    """
    Save transformed datasets to data/processed/.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # CONDITIONS
    data["conditions"].to_csv(
        PROCESSED_DIR / "conditions_processed.csv",
        index=False
    )

    data["condition_codes"].to_csv(
        PROCESSED_DIR / "condition_codes.csv",
        index=False
    )

    # OBSERVATIONS
    data["observations"].to_csv(
        PROCESSED_DIR / "observations_processed.csv",
        index=False
    )

    data["observation_codes"].to_csv(
        PROCESSED_DIR / "observation_codes.csv",
        index=False
    )

    # MEDICATIONS
    data["medications"].to_csv(
        PROCESSED_DIR / "medications_processed.csv",
        index=False
    )

    data["medication_codes"].to_csv(
        PROCESSED_DIR / "medication_codes.csv",
        index=False
    )

    # PROCEDURES
    data["procedures"].to_csv(
        PROCESSED_DIR / "procedures_processed.csv",
        index=False
    )

    data["procedure_codes"].to_csv(
        PROCESSED_DIR / "procedure_codes.csv",
        index=False
    )

    # ALLERGIES
    data["allergies"].to_csv(
        PROCESSED_DIR / "allergies_processed.csv",
        index=False
    )

    data["allergy_codes"].to_csv(
        PROCESSED_DIR / "allergy_codes.csv",
        index=False
    )


# ---------------------------------------------------------
# TEST / RUN TRANSFORMATION
# ---------------------------------------------------------

if __name__ == "__main__":

    from extract import extract_all
    from clean import clean_all

    print("Starting extraction...")

    raw_data = extract_all()

    print("Extraction successful.")

    print("Starting cleaning...")

    cleaned_data = clean_all(raw_data)

    print("Cleaning successful.")

    print("Starting transformation...")

    transformed_data = transform_all(cleaned_data)

    save_transformed(transformed_data)

    print("\nTRANSFORMATION SUCCESSFUL")
    print("-------------------------")

    print(
        "CONDITIONS:",
        len(transformed_data["conditions"]),
        "rows"
    )

    print(
        "ConditionCode:",
        len(transformed_data["condition_codes"]),
        "rows"
    )

    print(
        "OBSERVATIONS:",
        len(transformed_data["observations"]),
        "rows"
    )

    print(
        "ObservationCode:",
        len(transformed_data["observation_codes"]),
        "rows"
    )

    print(
        "MEDICATIONS:",
        len(transformed_data["medications"]),
        "rows"
    )

    print(
        "MedicationCode:",
        len(transformed_data["medication_codes"]),
        "rows"
    )

    print(
        "PROCEDURES:",
        len(transformed_data["procedures"]),
        "rows"
    )

    print(
        "ProcedureCode:",
        len(transformed_data["procedure_codes"]),
        "rows"
    )

    print(
        "ALLERGIES:",
        len(transformed_data["allergies"]),
        "rows"
    )

    print(
        "AllergyCode:",
        len(transformed_data["allergy_codes"]),
        "rows"
    )

    print("\nProcessed files saved to:")
    print(PROCESSED_DIR)
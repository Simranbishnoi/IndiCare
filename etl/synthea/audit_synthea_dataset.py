"""
===============================================================================
IndiCare - Synthea Dataset Audit Pipeline
===============================================================================

Purpose:
    Validate and audit the synthetic healthcare dataset generated using
    Synthea before loading the data into the relational database and using
    it for machine learning.

Data Source:
    Synthea Synthetic Patient Generator

Expected raw data location:
    IndiCare/data/raw/

Expected files:
    - patients.csv
    - conditions.csv
    - observations.csv

This script does NOT generate synthetic data.
It only validates the generated Synthea CSV files.

===============================================================================
"""

from pathlib import Path
import pandas as pd


# =============================================================================
# DATASET AUDIT FUNCTION
# =============================================================================

def audit_synthea_dataset(data_path):
    """
    Performs a basic audit of the Synthea synthetic healthcare dataset.

    Checks:
        1. Total number of patients
        2. Cardiovascular condition records
        3. Unique patients with cardiovascular conditions
        4. Unique patients without cardiovascular conditions
        5. Coverage of important clinical features
    """

    print("=" * 70)
    print("        INDICARE - SYNTHEA DATASET AUDIT REPORT")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # STEP 1: LOAD RAW CSV FILES
    # -------------------------------------------------------------------------

    print("\n[1/4] Loading Synthea CSV files...")

    patients_file = data_path / "patients.csv"
    conditions_file = data_path / "conditions.csv"
    observations_file = data_path / "observations.csv"

    # Check that required files exist
    required_files = [
        patients_file,
        conditions_file,
        observations_file
    ]

    for file in required_files:
        if not file.exists():
            print(f"\nERROR: Required file not found:")
            print(f"      {file}")
            print("\nPlease place the Synthea CSV files inside:")
            print("      data/raw/")
            return

    patients = pd.read_csv(patients_file)
    conditions = pd.read_csv(conditions_file)
    observations = pd.read_csv(observations_file)

    total_patients = patients["Id"].nunique()

    print(f"      Patients CSV loaded successfully.")
    print(f"      Total unique patients: {total_patients:,}")

    print(f"      Patients rows:       {len(patients):,}")
    print(f"      Conditions rows:     {len(conditions):,}")
    print(f"      Observations rows:   {len(observations):,}")

    # -------------------------------------------------------------------------
    # STEP 2: CARDIOVASCULAR CONDITION AUDIT
    # -------------------------------------------------------------------------

    print("\n[2/4] Auditing cardiovascular conditions...")

    cardiac_keywords = [
        "Heart",
        "Hypertens",
        "Infarction",
        "Failure",
        "CAD",
        "Angina",
        "Atrial",
        "Atheroscler"
    ]

    keyword_pattern = "|".join(cardiac_keywords)

    heart_conditions = conditions[
        conditions["DESCRIPTION"].str.contains(
            keyword_pattern,
            case=False,
            na=False
        )
    ]

    total_cardiac_records = len(heart_conditions)

    heart_pids = set(
        heart_conditions["PATIENT"].dropna().unique()
    )

    positive_patients = len(heart_pids)
    negative_patients = total_patients - positive_patients

    positive_percentage = (
        positive_patients / total_patients * 100
        if total_patients > 0
        else 0
    )

    negative_percentage = (
        negative_patients / total_patients * 100
        if total_patients > 0
        else 0
    )

    print(
        f"      Cardiovascular condition records: "
        f"{total_cardiac_records:,}"
    )

    print(
        f"      Unique patients WITH cardiovascular conditions: "
        f"{positive_patients:,} ({positive_percentage:.1f}%)"
    )

    print(
        f"      Unique patients WITHOUT cardiovascular conditions: "
        f"{negative_patients:,} ({negative_percentage:.1f}%)"
    )

    # -------------------------------------------------------------------------
    # STEP 3: CLINICAL FEATURE COVERAGE
    # -------------------------------------------------------------------------

    print("\n[3/4] Auditing clinical feature coverage...")

    feature_queries = {
        "Systolic Blood Pressure": "Systolic Blood Pressure",
        "Diastolic Blood Pressure": "Diastolic Blood Pressure",
        "Heart Rate": "Heart rate",
        "Body Mass Index": "Body Mass Index",
        "Cholesterol": "Cholesterol",
        "Glucose": "Glucose"
    }

    print()

    for feature_name, query in feature_queries.items():

        matching_observations = observations[
            observations["DESCRIPTION"].str.contains(
                query,
                case=False,
                na=False
            )
        ]

        unique_patients = matching_observations["PATIENT"].nunique()

        coverage_percentage = (
            unique_patients / total_patients * 100
            if total_patients > 0
            else 0
        )

        print(
            f"      {feature_name:<28} "
            f"{unique_patients:>5,} patients "
            f"({coverage_percentage:>6.1f}%)"
        )

    # -------------------------------------------------------------------------
    # STEP 4: FINAL AUDIT SUMMARY
    # -------------------------------------------------------------------------

    print("\n[4/4] Dataset Audit Summary")

    print("-" * 70)

    print(f"      Total patients:                 {total_patients:,}")
    print(f"      Cardiovascular patients:        {positive_patients:,}")
    print(f"      Non-cardiovascular patients:    {negative_patients:,}")
    print(f"      Cardiovascular ratio:           {positive_percentage:.1f}%")
    print(f"      Non-cardiovascular ratio:       {negative_percentage:.1f}%")

    print("-" * 70)

    print("\nAUDIT COMPLETE.")

    print(
        "\nNOTE:"
        "\nThis audit currently identifies broad cardiovascular conditions"
        "\nusing condition-description keywords."
        "\n"
        "\nIt should NOT yet be treated as the final heart-attack target."
        "\nThe final ML target will be defined separately using the appropriate"
        "\nMyocardial Infarction condition/code."
    )

    print("=" * 70)


# =============================================================================
# MAIN PROGRAM
# =============================================================================

if __name__ == "__main__":

    # Find the IndiCare project root automatically.
    #
    # Current file:
    # IndiCare/
    #   etl/
    #     synthea/
    #       audit_synthea_dataset.py
    #
    # parents[0] -> synthea/
    # parents[1] -> etl/
    # parents[2] -> IndiCare/

    project_root = Path(__file__).resolve().parents[2]

    # Raw Synthea data location
    data_path = project_root / "data" / "raw"

    audit_synthea_dataset(data_path)
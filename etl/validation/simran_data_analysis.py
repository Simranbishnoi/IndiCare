import pandas as pd


# ============================================================
# PATIENTS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PATIENTS VALIDATION")
print("=" * 60)

# Load the raw Patients CSV.
patients = pd.read_csv("data/raw/synthea/patients.csv")

# Purpose: Check the size and source columns of the Patients dataset.
print("Patients shape:", patients.shape)
print("Patient columns:")
print(patients.columns.tolist())


# ------------------------------------------------------------
# Basic profiling
# Purpose: Check data types, row/column information,
# missing values, and unique-value counts.
# ------------------------------------------------------------
print("\nPatient info:")
print(patients.info())

print("\nPatient missing values:")
print(patients.isna().sum())

print("\nPatient unique values:")
print(patients.nunique())


# ------------------------------------------------------------
# Primary key validation
# Purpose: Check whether Id uniquely identifies every patient
# and whether it contains missing values.
# ------------------------------------------------------------
print("\nIs patient Id unique?", patients["Id"].is_unique)
print("Is patient Id missing?", patients["Id"].isna().any())

# Finding:
# Id is unique and non-null, so it is a valid candidate PK.


# ------------------------------------------------------------
# Sample values
# Purpose: Inspect actual source values before making
# transformation or schema decisions.
# ------------------------------------------------------------
print("\nPatient sample values:")
print(patients.head())


# ------------------------------------------------------------
# Categorical analysis
# Purpose: Understand observed categories and missing values
# in important demographic columns.
# ------------------------------------------------------------
print("\nUnique categorical values:")

for column in ["MARITAL", "RACE", "ETHNICITY", "GENDER", "STATE"]:
    print(f"\n{column}:")
    print(patients[column].value_counts(dropna=False))


# ------------------------------------------------------------
# Identifier validation
# Purpose: Check whether SSN, DRIVERS, and PASSPORT are
# unique and whether they contain missing values.
# ------------------------------------------------------------
print("\nIdentifier uniqueness:")

for column in ["SSN", "DRIVERS", "PASSPORT"]:
    print(
        column,
        "unique =", patients[column].is_unique,
        "missing =", patients[column].isna().sum()
    )

# Duplicate counts.
print("\nDuplicate SSN rows:", patients["SSN"].duplicated().sum())
print("Duplicate DRIVERS rows:", patients["DRIVERS"].duplicated().sum())
print("Duplicate PASSPORT rows:", patients["PASSPORT"].duplicated().sum())

# Show repeated SSN values.
duplicate_ssns = patients[patients["SSN"].duplicated(keep=False)]

print("\nDuplicated SSN values:")
print(duplicate_ssns["SSN"].value_counts())

# Finding:
# SSN has 26 duplicate occurrences.
# DRIVERS has 297 duplicate occurrences.
# PASSPORT has 85 duplicate occurrences.
# None of these fields is suitable as the patient PK.


# ------------------------------------------------------------
# Date validation
# Purpose: Parse the source DD-MM-YYYY dates and distinguish
# valid dates, genuine missing values, and invalid values.
# ------------------------------------------------------------
print("\nBirthdate examples:")
print(patients["BIRTHDATE"].head(10).tolist())

print("Deathdate examples:")
print(patients["DEATHDATE"].head(10).tolist())

birthdate_parsed = pd.to_datetime(
    patients["BIRTHDATE"],
    format="%d-%m-%Y",
    errors="coerce"
)

deathdate_parsed = pd.to_datetime(
    patients["DEATHDATE"],
    format="%d-%m-%Y",
    errors="coerce"
)

print("Invalid BIRTHDATE values:", birthdate_parsed.isna().sum())
print("Invalid DEATHDATE values:", deathdate_parsed.isna().sum())

# Distinguish originally missing DEATHDATE from invalid non-missing dates.
non_missing_deathdates = patients["DEATHDATE"].notna()

invalid_deathdates = (
    non_missing_deathdates & deathdate_parsed.isna()
)

print(
    "Originally missing DEATHDATE:",
    patients["DEATHDATE"].isna().sum()
)

print(
    "Invalid non-missing DEATHDATE:",
    invalid_deathdates.sum()
)

# Chronological consistency.
# Purpose: Check whether any patient has a death date before birth.
print(
    "Death before birth:",
    len(
        patients[
            deathdate_parsed < birthdate_parsed
        ]
    )
)

# Finding:
# BIRTHDATE has 0 invalid values.
# DEATHDATE has 5000 genuine missing values and 0 invalid
# non-missing values.
# 0 patients have death before birth.


# ------------------------------------------------------------
# Numeric summary
# Purpose: Inspect ranges and distributions of numeric fields.
# ------------------------------------------------------------
numeric_columns = [
    "FIPS",
    "ZIP",
    "LAT",
    "LON",
    "HEALTHCARE_EXPENSES",
    "HEALTHCARE_COVERAGE",
    "INCOME"
]

print("\nNumeric column summary:")

for column in numeric_columns:
    print(f"\n{column}:")
    print(patients[column].describe())


# ------------------------------------------------------------
# ZIP/FIPS analysis
# Purpose: Investigate geographic-code missing/special values
# and ZIP representation.
# ------------------------------------------------------------
print("\nZIP values:")
print(patients["ZIP"].value_counts().head(20))

print("\nFIPS values:")
print(patients["FIPS"].value_counts(dropna=False).head(20))

zip_zero_fips_missing = patients[
    (patients["ZIP"] == 0) &
    (patients["FIPS"].isna())
]

print(
    "ZIP=0 and FIPS missing:",
    len(zip_zero_fips_missing)
)

zip_lengths = patients["ZIP"].astype(str).str.len()

print("\nZIP length distribution:")
print(zip_lengths.value_counts().sort_index())

print("\nNon-zero ZIP summary:")
print(patients[patients["ZIP"] != 0]["ZIP"].describe())

# Finding:
# ZIP=0 and missing FIPS occur together for 1575 patients.
# ZIP length is 1 for 1575 records (the value 0) and 4 for
# 4883 records.
# Non-zero ZIP values range from 1001 to 2861.


# ------------------------------------------------------------
# Geographic coordinate validation
# Purpose: Check whether LAT/LON fall within valid geographic
# coordinate ranges.
# ------------------------------------------------------------
print(
    "\nInvalid LAT values:",
    len(
        patients[
            (patients["LAT"] < -90) |
            (patients["LAT"] > 90)
        ]
    )
)

print(
    "Invalid LON values:",
    len(
        patients[
            (patients["LON"] < -180) |
            (patients["LON"] > 180)
        ]
    )
)

# Finding:
# 0 invalid LAT values and 0 invalid LON values.


# ------------------------------------------------------------
# Monetary sanity checks
# Purpose: Check for negative healthcare expenses, coverage,
# and income.
# ------------------------------------------------------------
print(
    "\nNegative healthcare expenses:",
    len(
        patients[
            patients["HEALTHCARE_EXPENSES"] < 0
        ]
    )
)

print(
    "Negative healthcare coverage:",
    len(
        patients[
            patients["HEALTHCARE_COVERAGE"] < 0
        ]
    )
)

print(
    "Negative income:",
    len(
        patients[
            patients["INCOME"] < 0
        ]
    )
)

print(
    "Zero healthcare coverage:",
    len(
        patients[
            patients["HEALTHCARE_COVERAGE"] == 0
        ]
    )
)

print(
    "Coverage greater than expenses:",
    len(
        patients[
            patients["HEALTHCARE_COVERAGE"] >
            patients["HEALTHCARE_EXPENSES"]
        ]
    )
)

# Findings:
# No negative values were found in the three monetary fields.
# 137 patients have zero healthcare coverage.
# 3598 patients have coverage greater than expenses.
# The latter is treated as an observed pattern, not an error.


# ------------------------------------------------------------
# Core text-field quality
# Purpose: Check whether FIRST and LAST contain empty or
# whitespace-only strings in addition to checking NaN values.
# ------------------------------------------------------------
print(
    "\nEmpty/whitespace FIRST:",
    len(
        patients[
            patients["FIRST"].astype(str).str.strip() == ""
        ]
    )
)

print(
    "Empty/whitespace LAST:",
    len(
        patients[
            patients["LAST"].astype(str).str.strip() == ""
        ]
    )
)

# Finding:
# FIRST and LAST have no empty/whitespace-only values.


# ============================================================
# PATIENTS — PROVISIONAL COLUMN DECISIONS
# ============================================================
#
# KEEP:
# Id, FIRST, LAST, BIRTHDATE, DEATHDATE, MARITAL, RACE,
# ETHNICITY, GENDER, COUNTY, FIPS, ZIP, LAT, LON
#
# TRANSFORM:
# BIRTHDATE and DEATHDATE -> DATE
# FIPS and ZIP -> appropriate geographic-code representation
#
# EXCLUDE FROM CURRENT PROCESSED CLINICAL TABLE:
# SSN, DRIVERS, PASSPORT, PREFIX, MIDDLE, SUFFIX, MAIDEN,
# BIRTHPLACE, ADDRESS, CITY, STATE, HEALTHCARE_EXPENSES,
# HEALTHCARE_COVERAGE, INCOME
#
# DERIVED LATER:
# AGE -> derive from BIRTHDATE when required.
#
# Raw CSV files remain unchanged.
# =====================================================
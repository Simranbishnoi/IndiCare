
import pandas as pd


# ============================================================
# PATIENTS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PATIENTS VALIDATION")
print("=" * 60)

# Load the raw Patients CSV.
patients = pd.read_csv("data/raw/synthea/patients.csv")
'''
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
'''
#==========================================
# ============================================================
# ENCOUNTERS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("ENCOUNTERS VALIDATION")
print("=" * 60)

# Load the raw Encounters CSV.
encounters = pd.read_csv("data/raw/synthea/encounters.csv")

'''
# ------------------------------------------------------------
# 1. BASIC PROFILING
# ------------------------------------------------------------
# Purpose:
# Understand the structure of the Encounters table before
# performing detailed validation.
# ------------------------------------------------------------

print("Encounters shape:", encounters.shape)

# OUTPUT:
# (532458, 15)
#
# Finding:
# The Encounters table contains 532,458 rows and 15 columns.


print("\nEncounter columns:")
print(encounters.columns.tolist())

# OUTPUT:
# [
#   'Id',
#   'START',
#   'STOP',
#   'PATIENT',
#   'ORGANIZATION',
#   'PROVIDER',
#   'PAYER',
#   'ENCOUNTERCLASS',
#   'CODE',
#   'DESCRIPTION',
#   'BASE_ENCOUNTER_COST',
#   'TOTAL_CLAIM_COST',
#   'PAYER_COVERAGE',
#   'REASONCODE',
#   'REASONDESCRIPTION'
# ]
#
# Finding:
# These are the 15 source columns present in Encounters.


print("\nEncounter info:")
print(encounters.info())

# Finding:
# The table contains identifier, datetime, categorical,
# reference, and financial fields.
#
# START and STOP are initially stored as strings.
# REASONCODE and REASONDESCRIPTION contain missing values.
# The remaining important fields are populated.


print("\nEncounter missing values:")
print(encounters.isna().sum())

# Important output:
# REASONCODE           197267
# REASONDESCRIPTION    197267
# All other columns    0
#
# Finding:
# Only REASONCODE and REASONDESCRIPTION contain missing values.
# Their missingness is investigated separately below.


print("\nEncounter unique values:")
print(encounters.nunique())

# Important output:
# Id                     532458
# START                  523339
# STOP                   531616
# PATIENT                  6458
# ORGANIZATION             1123
# PROVIDER                 1123
# PAYER                      10
# ENCOUNTERCLASS             10
# CODE                       60
# DESCRIPTION                60
# BASE_ENCOUNTER_COST        11
# TOTAL_CLAIM_COST       100428
# PAYER_COVERAGE          98401
# REASONCODE                173
# REASONDESCRIPTION         173
#
# Finding:
# There are 6,458 unique patients represented across the
# 532,458 encounter records.
# There are 1,123 organizations and 1,123 providers.
# There are 10 payers and 10 encounter classes.
# There are 60 encounter codes/descriptions and 173
# reason codes/descriptions.


# ------------------------------------------------------------
# 2. PRIMARY KEY VALIDATION
# ------------------------------------------------------------
# Purpose:
# Check whether Encounters.Id can uniquely identify every
# encounter and whether it contains missing values.
# ------------------------------------------------------------

print(
    "Is encounter Id unique?",
    encounters["Id"].is_unique
)

print(
    "Is encounter Id missing?",
    encounters["Id"].isna().any()
)

# OUTPUT:
# Is encounter Id unique? True
# Is encounter Id missing? False
#
# Finding:
# Encounters.Id is unique and non-null.
# Therefore, Id is a valid candidate primary key.


# ------------------------------------------------------------
# 3. PATIENT FOREIGN KEY VALIDATION
# ------------------------------------------------------------
# Purpose:
# Verify that every encounter has a patient reference and
# that every referenced patient exists in PATIENTS.Id.
# ------------------------------------------------------------

print(
    "Missing encounter PATIENT values:",
    encounters["PATIENT"].isna().sum()
)

# OUTPUT:
# Missing encounter PATIENT values: 0
#
# Finding:
# Every encounter contains a patient ID.


print(
    "Invalid encounter patient references:",
    len(
        encounters[
            ~encounters["PATIENT"].isin(patients["Id"])
        ]
    )
)

# OUTPUT:
# Invalid encounter patient references: 0
#
# Finding:
# Every ENCOUNTERS.PATIENT value exists in PATIENTS.Id.
#
# Therefore:
# ENCOUNTERS.PATIENT can reference PATIENTS.Id as a foreign key.


# ------------------------------------------------------------
# 4. START / STOP DATE VALIDATION
# ------------------------------------------------------------
# Purpose:
# Validate the encounter timestamps and make sure an encounter
# does not end before it starts.
# ------------------------------------------------------------

print("START examples:")
print(encounters["START"].head().tolist())

print("STOP examples:")
print(encounters["STOP"].head().tolist())

# OUTPUT:
# START examples:
# 1993-08-18T18:21:08Z
# 1968-06-28T10:52:28Z
# 1983-06-13T15:33:48Z
# ...
#
# STOP examples:
# 1993-08-18T18:49:06Z
# 1968-06-28T11:35:54Z
# 1983-06-13T15:48:48Z
# ...
#
# Finding:
# START and STOP are ISO-style timestamps containing date,
# time, and a UTC indicator (Z).


start_parsed = pd.to_datetime(
    encounters["START"],
    errors="coerce",
    utc=True
)

stop_parsed = pd.to_datetime(
    encounters["STOP"],
    errors="coerce",
    utc=True
)

print(
    "Invalid START values:",
    start_parsed.isna().sum()
)

print(
    "Invalid STOP values:",
    stop_parsed.isna().sum()
)

# OUTPUT:
# Invalid START values: 0
# Invalid STOP values: 0
#
# Finding:
# All START and STOP values can be successfully parsed as
# datetime values.


print(
    "Encounters with STOP before START:",
    len(
        encounters[
            stop_parsed < start_parsed
        ]
    )
)

# OUTPUT:
# Encounters with STOP before START: 0
#
# Finding:
# No encounter has a STOP timestamp earlier than its START.
# Therefore, the chronological relationship is valid.
#
# Provisional ETL decision:
# START and STOP should be transformed from source strings
# into appropriate database timestamp types.


# ------------------------------------------------------------
# 5. ENCOUNTER CLASS VALIDATION
# ------------------------------------------------------------
# Purpose:
# Identify all encounter categories and check for missing
# encounter classes.
# ------------------------------------------------------------

print("Encounter classes:")
print(
    encounters["ENCOUNTERCLASS"].value_counts(
        dropna=False
    )
)

# OUTPUT:
# ambulatory    309061
# wellness       96362
# outpatient     60080
# urgentcare     28687
# emergency      16474
# inpatient      10860
# home            6574
# hospice         1855
# snf             1489
# virtual         1016
#
# Finding:
# There are 10 encounter classes and no missing values.
#
# Provisional ETL decision:
# ENCOUNTERCLASS should be retained as an encounter
# classification attribute.


# ------------------------------------------------------------
# 6. CODE / DESCRIPTION MAPPING
# ------------------------------------------------------------
# Purpose:
# Determine whether each encounter CODE consistently maps
# to exactly one DESCRIPTION.
# ------------------------------------------------------------

code_description_counts = (
    encounters
    .groupby("CODE")["DESCRIPTION"]
    .nunique()
)

print(code_description_counts)

# OUTPUT:
# Every CODE has a value of 1.
#
# Finding:
# Every CODE maps to exactly one DESCRIPTION.


print(
    "Missing encounter CODE:",
    encounters["CODE"].isna().sum()
)

print(
    "Missing encounter DESCRIPTION:",
    encounters["DESCRIPTION"].isna().sum()
)

# OUTPUT:
# Missing encounter CODE: 0
# Missing encounter DESCRIPTION: 0
#
# Finding:
# CODE and DESCRIPTION are complete.


description_code_counts = (
    encounters
    .groupby("DESCRIPTION")["CODE"]
    .nunique()
)

print(description_code_counts)

# OUTPUT:
# Every DESCRIPTION has a value of 1.
#
# Finding:
# Every DESCRIPTION maps to exactly one CODE.
#
# Therefore, in this dataset:
#
# CODE <-> DESCRIPTION
#
# forms a one-to-one mapping.
#
# Normalization consideration:
# CODE and DESCRIPTION can be considered for a separate
# encounter-code lookup/reference table to avoid repeated
# descriptions in the Encounters table.


# ------------------------------------------------------------
# 7. ORGANIZATION / PROVIDER VALIDATION
# ------------------------------------------------------------
# Purpose:
# Determine whether ORGANIZATION and PROVIDER are separate
# identifiers and investigate their relationship.
# ------------------------------------------------------------

print(
    "Organization/Provider identical:",
    (
        encounters["ORGANIZATION"] ==
        encounters["PROVIDER"]
    ).all()
)

# OUTPUT:
# Organization/Provider identical: False
#
# Finding:
# ORGANIZATION and PROVIDER are not identical columns.
# They should therefore be treated as separate entities/
# references.


print(
    "Missing ORGANIZATION:",
    encounters["ORGANIZATION"].isna().sum()
)

print(
    "Missing PROVIDER:",
    encounters["PROVIDER"].isna().sum()
)

# OUTPUT:
# Missing ORGANIZATION: 0
# Missing PROVIDER: 0
#
# Finding:
# Every encounter contains both an organization ID and
# provider ID.


provider_org_counts = (
    encounters
    .groupby("PROVIDER")["ORGANIZATION"]
    .nunique()
)

print(provider_org_counts)

# OUTPUT:
# All 1,123 providers have a value of 1.
#
# Finding:
# Each provider is associated with exactly one organization
# in this dataset.
#
# Observed relationship:
#
# ORGANIZATION 1 ----< PROVIDER
#
# More precisely:
# PROVIDER -> ORGANIZATION is many-to-one.
#
# Provisional ETL/schema decision:
# PROVIDER and ORGANIZATION should be retained as separate
# entity/reference fields.
#
# Note:
# We have not yet verified these IDs against separate
# organization/provider master tables.


# ------------------------------------------------------------
# 8. PAYER VALIDATION
# ------------------------------------------------------------
# Purpose:
# Understand payer values, check completeness, and determine
# whether payer should be represented at patient or encounter
# level.
# ------------------------------------------------------------

print("Payer values:")
print(
    encounters["PAYER"].value_counts(
        dropna=False
    )
)

# OUTPUT:
# 10 distinct payer IDs.
# No NaN value.
#
# Finding:
# There are 10 payer identifiers and every encounter has
# a payer value.


patient_payer_counts = (
    encounters
    .groupby("PATIENT")["PAYER"]
    .nunique()
)

print("\nNumber of patients by number of payers:")
print(
    patient_payer_counts
    .value_counts()
    .sort_index()
)

# OUTPUT:
# 1 payer    -> 1202 patients
# 2 payers   -> 2540 patients
# 3 payers   -> 1687 patients
# 4 payers   -> 775 patients
# 5 payers   -> 230 patients
# 6 payers   -> 24 patients
#
# Finding:
# Patients can have multiple payers across their encounters.
#
# 1,202 patients have one payer.
# 5,256 patients have two or more payers.
#
# Therefore, PAYER should not be stored as a single fixed
# attribute in PATIENTS.
#
# PAYER is appropriately associated with ENCOUNTERS.
#
# Provisional schema decision:
# PAYER should be retained at the encounter level and can
# potentially reference a separate payer entity/lookup table.


# ------------------------------------------------------------
# 9. FINANCIAL VALIDATION
# ------------------------------------------------------------
# Purpose:
# Check the encounter financial fields for missing values,
# negative values, and basic logical inconsistencies.
# ------------------------------------------------------------

print(
    "Missing BASE_ENCOUNTER_COST:",
    encounters["BASE_ENCOUNTER_COST"].isna().sum()
)

print(
    "Missing TOTAL_CLAIM_COST:",
    encounters["TOTAL_CLAIM_COST"].isna().sum()
)

print(
    "Missing PAYER_COVERAGE:",
    encounters["PAYER_COVERAGE"].isna().sum()
)

# OUTPUT:
# Missing BASE_ENCOUNTER_COST: 0
# Missing TOTAL_CLAIM_COST: 0
# Missing PAYER_COVERAGE: 0
#
# Finding:
# All three financial fields are complete.


print(
    "Negative BASE_ENCOUNTER_COST:",
    len(
        encounters[
            encounters["BASE_ENCOUNTER_COST"] < 0
        ]
    )
)

print(
    "Negative TOTAL_CLAIM_COST:",
    len(
        encounters[
            encounters["TOTAL_CLAIM_COST"] < 0
        ]
    )
)

print(
    "Negative PAYER_COVERAGE:",
    len(
        encounters[
            encounters["PAYER_COVERAGE"] < 0
        ]
    )
)

# OUTPUT:
# Negative BASE_ENCOUNTER_COST: 0
# Negative TOTAL_CLAIM_COST: 0
# Negative PAYER_COVERAGE: 0
#
# Finding:
# No negative values were found in any of the three
# financial fields.


print(
    "Total claim cost less than base encounter cost:",
    len(
        encounters[
            encounters["TOTAL_CLAIM_COST"] <
            encounters["BASE_ENCOUNTER_COST"]
        ]
    )
)

# OUTPUT:
# Total claim cost less than base encounter cost: 1
#
# Finding:
# One encounter violates the expected relationship
# TOTAL_CLAIM_COST >= BASE_ENCOUNTER_COST.


suspicious_cost = encounters[
    encounters["TOTAL_CLAIM_COST"] <
    encounters["BASE_ENCOUNTER_COST"]
]

print(
    suspicious_cost[
        [
            "Id",
            "PATIENT",
            "START",
            "STOP",
            "ENCOUNTERCLASS",
            "BASE_ENCOUNTER_COST",
            "TOTAL_CLAIM_COST",
            "PAYER_COVERAGE"
        ]
    ]
)

# OUTPUT for the suspicious encounter:
# BASE_ENCOUNTER_COST = 85.55
# TOTAL_CLAIM_COST    = 0.00
# PAYER_COVERAGE      = 0.00
#
# Finding:
# One financial consistency anomaly was identified and
# inspected.
#
# It should be flagged/documented rather than automatically
# deleted because the available data does not establish that
# this record is definitively invalid.


print(
    "Payer coverage greater than total claim cost:",
    len(
        encounters[
            encounters["PAYER_COVERAGE"] >
            encounters["TOTAL_CLAIM_COST"]
        ]
    )
)

# OUTPUT:
# Payer coverage greater than total claim cost: 0
#
# Finding:
# No encounter has payer coverage greater than its total
# claim cost.


# ------------------------------------------------------------
# 10. REASON CODE / DESCRIPTION VALIDATION
# ------------------------------------------------------------
# Purpose:
# Check whether REASONCODE and REASONDESCRIPTION have
# consistent missingness and whether reason codes map
# consistently to descriptions.
# ------------------------------------------------------------

print(
    "Reason code/description missing mismatch:",
    len(
        encounters[
            encounters["REASONCODE"].isna() !=
            encounters["REASONDESCRIPTION"].isna()
        ]
    )
)

# OUTPUT:
# Reason code/description missing mismatch: 0
#
# Finding:
# REASONCODE and REASONDESCRIPTION are always missing or
# present together.
#
# The 197,267 missing reason-code records therefore have
# matching missing reason descriptions.


reason_code_description = (
    encounters
    .dropna(subset=["REASONCODE"])
    .groupby("REASONCODE")["REASONDESCRIPTION"]
    .nunique()
)

print(reason_code_description)

# OUTPUT:
# Every non-missing REASONCODE has a value of 1.
#
# Finding:
# Every non-missing REASONCODE maps to exactly one
# REASONDESCRIPTION.


print(
    "REASONCODEs with multiple descriptions:",
    (reason_code_description > 1).sum()
)

# OUTPUT:
# REASONCODEs with multiple descriptions: 0
#
# Finding:
# No REASONCODE maps to multiple descriptions.
#
# Provisional normalization consideration:
# REASONCODE and REASONDESCRIPTION can be represented in a
# separate reason lookup/reference table.


# ============================================================
# ENCOUNTERS — PROVISIONAL COLUMN DECISIONS
# ============================================================
#
# KEEP:
# Id
# START
# STOP
# PATIENT
# ORGANIZATION
# PROVIDER
# PAYER
# ENCOUNTERCLASS
# CODE
# BASE_ENCOUNTER_COST
# TOTAL_CLAIM_COST
# PAYER_COVERAGE
# REASONCODE
#
# TRANSFORM:
# START -> database timestamp
# STOP -> database timestamp
#
# NORMALIZE / REFERENCE:
# CODE <-> DESCRIPTION
# REASONCODE -> REASONDESCRIPTION
# PROVIDER -> ORGANIZATION
# PAYER -> payer entity/lookup
#
# DESCRIPTION:
# Move to an encounter-code lookup/reference table rather
# than repeating the same description in every encounter.
#
# REASONDESCRIPTION:
# Move to a reason lookup/reference table rather than
# repeating the same description in every encounter.
#
# FINANCIAL ANOMALY:
# One encounter has:
# BASE_ENCOUNTER_COST = 85.55
# TOTAL_CLAIM_COST = 0.00
# PAYER_COVERAGE = 0.00
#
# This should be documented/flagged and not automatically
# deleted without a defined business rule.
#
# RAW DATA:
# The raw Encounters CSV remains unchanged.
# ============================================================
'''
# ============================================================
# CAREPLANS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("CAREPLANS VALIDATION")
print("=" * 60)

careplans = pd.read_csv("data/raw/synthea/careplans.csv")


# ------------------------------------------------------------
# 1. BASIC STRUCTURE
# ------------------------------------------------------------
# Purpose:
# Understand the size, columns, data types, missing values,
# and unique values in the CarePlans table.
# ------------------------------------------------------------

print("CarePlans shape:", careplans.shape)

# OUTPUT:
# CarePlans shape: (26149, 9)
#
# Finding:
# The CarePlans table contains 26,149 rows and 9 columns.


print("\nCarePlans columns:")
print(careplans.columns.tolist())

# OUTPUT:
# ['Id', 'START', 'STOP', 'PATIENT', 'ENCOUNTER',
#  'CODE', 'DESCRIPTION', 'REASONCODE', 'REASONDESCRIPTION']
#
# Finding:
# CarePlans contains identifiers, dates, patient and encounter
# references, care-plan codes/descriptions, and reason information.


print("\nCarePlans info:")
print(careplans.info())

# OUTPUT:
# Id                   26149 non-null
# START                26149 non-null
# STOP                  9789 non-null
# PATIENT              26149 non-null
# ENCOUNTER            26149 non-null
# CODE                 26149 non-null
# DESCRIPTION          26149 non-null
# REASONCODE           16665 non-null
# REASONDESCRIPTION    16665 non-null
#
# Finding:
# START, PATIENT, ENCOUNTER, CODE, DESCRIPTION, and Id are
# completely populated.
#
# STOP has 16,360 missing values.
# REASONCODE and REASONDESCRIPTION each have 9,484 missing
# values.


print("\nCarePlans missing values:")
print(careplans.isna().sum())

# OUTPUT:
# Id                       0
# START                    0
# STOP                 16360
# PATIENT                  0
# ENCOUNTER                0
# CODE                     0
# DESCRIPTION              0
# REASONCODE            9484
# REASONDESCRIPTION     9484
#
# Finding:
# Missingness is concentrated in STOP and the two reason fields.


print("\nCarePlans unique values:")
print(careplans.nunique())

# OUTPUT:
# Id                   26149
# START                13305
# STOP                  4834
# PATIENT               6333
# ENCOUNTER            25673
# CODE                    39
# DESCRIPTION             39
# REASONCODE              62
# REASONDESCRIPTION       62
#
# Finding:
# There are 26,149 CarePlan records and 6,333 unique patients.
# There are 25,673 unique encounter references.
# There are 39 CarePlan codes/descriptions and 62 reason
# codes/descriptions.


# ------------------------------------------------------------
# 2. PRIMARY KEY VALIDATION
# ------------------------------------------------------------
# Purpose:
# Check whether CarePlans.Id can uniquely identify every
# CarePlan.
# ------------------------------------------------------------

print(
    "Is CarePlan Id unique?",
    careplans["Id"].is_unique
)

print(
    "Missing CarePlan Id:",
    careplans["Id"].isna().sum()
)

# OUTPUT:
# Is CarePlan Id unique? True
# Missing CarePlan Id: 0
#
# Finding:
# CarePlans.Id is unique and non-null.
# Therefore, Id is a valid primary-key candidate.


# ------------------------------------------------------------
# 3. PATIENT FOREIGN KEY VALIDATION
# ------------------------------------------------------------
# Purpose:
# Verify that every CarePlan has a patient reference and that
# every referenced patient exists in PATIENTS.Id.
# ------------------------------------------------------------

print(
    "Missing CarePlan PATIENT:",
    careplans["PATIENT"].isna().sum()
)

# OUTPUT:
# Missing CarePlan PATIENT: 0
#
# Finding:
# Every CarePlan contains a patient ID.


print(
    "Invalid CarePlan patient references:",
    len(
        careplans[
            ~careplans["PATIENT"].isin(patients["Id"])
        ]
    )
)

# OUTPUT:
# Invalid CarePlan patient references: 0
#
# Finding:
# Every CarePlan patient ID exists in PATIENTS.Id.
#
# Therefore:
# CAREPLANS.PATIENT → PATIENTS.Id
# can be represented as a foreign-key relationship.


# ------------------------------------------------------------
# 4. ENCOUNTER FOREIGN KEY VALIDATION
# ------------------------------------------------------------
# Purpose:
# Verify that every CarePlan has an encounter reference and
# that every referenced encounter exists in ENCOUNTERS.Id.
# ------------------------------------------------------------

print(
    "Missing CarePlan ENCOUNTER:",
    careplans["ENCOUNTER"].isna().sum()
)

# OUTPUT:
# Missing CarePlan ENCOUNTER: 0
#
# Finding:
# Every CarePlan contains an encounter ID.


print(
    "Invalid CarePlan encounter references:",
    len(
        careplans[
            ~careplans["ENCOUNTER"].isin(encounters["Id"])
        ]
    )
)

# OUTPUT:
# Invalid CarePlan encounter references: 0
#
# Finding:
# Every CarePlan encounter ID exists in ENCOUNTERS.Id.
#
# Therefore:
# CAREPLANS.ENCOUNTER → ENCOUNTERS.Id
# can be represented as a foreign-key relationship.


# ------------------------------------------------------------
# 5. START / STOP DATE VALIDATION
# ------------------------------------------------------------
# Purpose:
# Validate CarePlan dates and check whether the chronological
# relationship between START and STOP is valid.
# ------------------------------------------------------------

print("START examples:")
print(careplans["START"].head().tolist())

print("STOP examples:")
print(careplans["STOP"].dropna().head().tolist())

# OUTPUT:
# START examples:
# ['1993-08-18', '2002-07-31', '1990-05-11',
#  '1995-10-07', '2016-10-31']
#
# STOP examples:
# ['2017-01-02', '2021-01-29', '2021-02-27',
#  '2026-06-04', '2020-06-05']
#
# Finding:
# CarePlan START and STOP values use a date-only format:
# YYYY-MM-DD.


start_parsed = pd.to_datetime(
    careplans["START"],
    errors="coerce"
)

stop_parsed = pd.to_datetime(
    careplans["STOP"],
    errors="coerce"
)

print(
    "Invalid CarePlan START values:",
    start_parsed.isna().sum()
)

# OUTPUT:
# Invalid CarePlan START values: 0
#
# Finding:
# All START values can be successfully parsed as dates.


print(
    "Originally missing CarePlan STOP:",
    careplans["STOP"].isna().sum()
)

# OUTPUT:
# Originally missing CarePlan STOP: 16360
#
# Finding:
# 16,360 CarePlans do not have a STOP date in the source data.
# These values are missing, not automatically invalid.


print(
    "Invalid non-missing CarePlan STOP:",
    (
        careplans["STOP"].notna() &
        stop_parsed.isna()
    ).sum()
)

# OUTPUT:
# Invalid non-missing CarePlan STOP: 0
#
# Finding:
# None of the provided STOP dates are malformed.


print(
    "CarePlans with STOP before START:",
    len(
        careplans[
            stop_parsed < start_parsed
        ]
    )
)

# OUTPUT:
# CarePlans with STOP before START: 0
#
# Finding:
# No CarePlan has a STOP date earlier than its START date.
#
# Provisional ETL decision:
# START → DATE
# STOP  → nullable DATE


# ------------------------------------------------------------
# 6. CAREPLAN CODE / DESCRIPTION VALIDATION
# ------------------------------------------------------------
# Purpose:
# Determine whether each CarePlan CODE consistently maps to
# one DESCRIPTION.
# ------------------------------------------------------------

careplan_code_description = (
    careplans
    .groupby("CODE")["DESCRIPTION"]
    .nunique()
)

print(careplan_code_description)

# OUTPUT:
# All 39 CODE values have a result of 1.
#
# Finding:
# Every CarePlan CODE maps to exactly one DESCRIPTION.


careplan_description_code = (
    careplans
    .groupby("DESCRIPTION")["CODE"]
    .nunique()
)

print(careplan_description_code)

# OUTPUT:
# All 39 DESCRIPTION values have a result of 1.
#
# Finding:
# Every DESCRIPTION maps to exactly one CODE.
#
# Therefore:
# CODE ↔ DESCRIPTION
# is a one-to-one mapping in this dataset.


# ------------------------------------------------------------
# 7. REASON CODE / DESCRIPTION VALIDATION
# ------------------------------------------------------------
# Purpose:
# Check whether REASONCODE and REASONDESCRIPTION have
# consistent missingness.
# ------------------------------------------------------------

print(
    "Reason code/description missing mismatch:",
    len(
        careplans[
            careplans["REASONCODE"].isna() !=
            careplans["REASONDESCRIPTION"].isna()
        ]
    )
)

# OUTPUT:
# Reason code/description missing mismatch: 0
#
# Finding:
# REASONCODE and REASONDESCRIPTION are always missing or
# present together.
#
# There are 9,484 CarePlans where both reason fields are
# missing.


# ------------------------------------------------------------
# 8. REASONCODE → REASONDESCRIPTION MAPPING
# ------------------------------------------------------------
# Purpose:
# Determine whether every non-missing REASONCODE consistently
# maps to one REASONDESCRIPTION.
# ------------------------------------------------------------

careplan_reason_description = (
    careplans
    .dropna(subset=["REASONCODE"])
    .groupby("REASONCODE")["REASONDESCRIPTION"]
    .nunique()
)

print(careplan_reason_description)

# OUTPUT:
# 62 REASONCODE values were found.
# Every REASONCODE has a value of 1.
#
# Finding:
# Every non-missing REASONCODE maps to exactly one
# REASONDESCRIPTION.


print(
    "REASONCODEs with multiple descriptions:",
    (careplan_reason_description > 1).sum()
)

# OUTPUT:
# REASONCODEs with multiple descriptions: 0
#
# Finding:
# No REASONCODE maps to multiple descriptions.


# ------------------------------------------------------------
# 9. CAREPLAN ↔ ENCOUNTER DATE INSPECTION
# ------------------------------------------------------------
# Purpose:
# Inspect the relationship between CarePlan dates and the
# dates of their associated encounters.
#
# We do NOT impose a strict rule that a CarePlan START must
# fall inside the associated encounter period because the
# source data does not establish such a business rule.
# ------------------------------------------------------------

encounter_dates = encounters[
    ["Id", "START", "STOP"]
].copy()

encounter_dates["START"] = pd.to_datetime(
    encounter_dates["START"],
    errors="coerce",
    utc=True
)

encounter_dates["STOP"] = pd.to_datetime(
    encounter_dates["STOP"],
    errors="coerce",
    utc=True
)

careplans["START_PARSED"] = pd.to_datetime(
    careplans["START"],
    errors="coerce"
)

careplan_with_encounter = careplans.merge(
    encounter_dates,
    left_on="ENCOUNTER",
    right_on="Id",
    how="left",
    suffixes=("_CAREPLAN", "_ENCOUNTER")
)

print(
    careplan_with_encounter[
        [
            "ENCOUNTER",
            "START_PARSED",
            "START_ENCOUNTER",
            "STOP_ENCOUNTER"
        ]
    ].head(10).to_string(index=False)
)

# OBSERVED OUTPUT:
# CarePlan START dates were sometimes the same calendar date
# as the associated encounter and sometimes the following
# calendar date.
#
# Examples:
#
# CarePlan START     Encounter START
# 1993-08-18         1993-08-18 18:21:08+00:00
# 2002-07-31         2002-07-30 18:32:44+00:00
# 1990-05-11         1990-05-11 10:52:28+00:00
# 1995-10-07         1995-10-07 18:09:54+00:00
# 2016-10-31         2016-10-30 18:45:28+00:00
#
# Finding:
# CarePlan START may occur on the same calendar date as, or
# after, the associated encounter date.
#
# No strict CarePlan START/STOP versus Encounter START/STOP
# constraint was imposed because the source data does not
# establish such a business rule.


# ============================================================
# CAREPLANS — PROVISIONAL COLUMN DECISIONS
# ============================================================
#
# KEEP:
# Id
# START
# STOP
# PATIENT
# ENCOUNTER
# CODE
# REASONCODE
#
# TRANSFORM:
# START → DATE
# STOP  → nullable DATE
#
# NORMALIZE / REFERENCE:
# CODE + DESCRIPTION
# REASONCODE + REASONDESCRIPTION
#
# PRIMARY KEY:
# Id
#
# FOREIGN KEYS:
# PATIENT   → PATIENTS.Id
# ENCOUNTER → ENCOUNTERS.Id
#
# POTENTIAL LOOKUP TABLES:
#
# CAREPLAN_TYPES
# ----------------
# CODE (PK)
# DESCRIPTION
#
# CAREPLAN_REASONS
# ----------------
# REASONCODE (PK)
# REASONDESCRIPTION
#
# MISSING DATA:
# STOP has 16,360 missing values.
# REASONCODE and REASONDESCRIPTION have 9,484 missing
# values each.
#
# These missing values are not automatically deleted.
#
# DATE RELATIONSHIP:
# No strict CarePlan-to-Encounter date constraint is imposed.
#
# RAW DATA:
# The raw CarePlans CSV remains unchanged.
# ============================================================
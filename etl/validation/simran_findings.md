IndiCare Data Validation Findings

Scope

This document records the validation findings for the three tables assigned
to Teammate 1:

PATIENTS

ENCOUNTERS

CAREPLANS

The raw Synthea CSV files remain unchanged. Validation findings are used to
support later schema and ETL decisions.

1. PATIENTS

1.1 Dataset Profile

Rows: 6,458

Columns: 28

1.2 Primary Key Validation

Id

Checks performed:

Uniqueness using is_unique

Missing values using isna()

Result:

Unique: True

Missing: False

Finding: patients.Id is a valid candidate primary key.

1.3 Missing Values

Important missing-value counts:

Column

Missing

DEATHDATE

5,000

DRIVERS

77

PASSPORT

86

PREFIX

84

MIDDLE

1,308

SUFFIX

6,353

MAIDEN

3,909

MARITAL

122

FIPS

1,575

All other patient columns have zero missing values.

Conclusion: Missing values are preserved as information and will be handled
during ETL/schema implementation where appropriate. Missingness alone is not
treated as a reason to remove a column.

1.4 Categorical Findings

MARITAL

M: 3,571

S: 1,253

D: 1,112

W: 400

Missing: 122

Decision: Retain as a demographic attribute for the current database scope.

RACE

white: 5,279

black: 605

asian: 381

hawaiian: 86

other: 77

native: 30

Missing: 0

Decision: Retain.

ETHNICITY

nonhispanic: 5,713

hispanic: 745

Missing: 0

Decision: Retain.

GENDER

M: 3,250

F: 3,208

Missing: 0

Decision: Retain.

STATE

Massachusetts: 6,458

Missing: 0

Finding: The current dataset contains only Massachusetts.

Provisional decision: Exclude from the processed clinical table because it
provides no variation in this dataset. This is dataset-specific.

1.5 Identifier Findings

Column

Missing

Unique?

Duplicate occurrences

SSN

0

No

26

DRIVERS

77

No

297

PASSPORT

86

No

85

Finding: None of these fields can serve as the patient primary key.

Provisional decision: Exclude SSN, DRIVERS, and PASSPORT from the
current processed clinical patient table because they are administrative
identifiers outside the current clinical scope.

The raw source remains unchanged.

1.6 Name Fields

Column

Missing

Decision

FIRST

0

Retain

LAST

0

Retain

MIDDLE

1,308

Exclude

PREFIX

84

Exclude

SUFFIX

6,353

Exclude

MAIDEN

3,909

Exclude

Additional validation:

Empty/whitespace-only FIRST: 0

Empty/whitespace-only LAST: 0

Conclusion: Retain core first and last names. Optional name components are
not required for the current clinical database scope.

1.7 Date Validation

BIRTHDATE

Source format: DD-MM-YYYY

Missing: 0

Invalid values: 0

Decision: Retain and transform to database DATE.

DEATHDATE

Source format: DD-MM-YYYY

Missing: 5,000

Invalid non-missing values: 0

Decision: Retain and transform to nullable database DATE.

Chronological consistency

Checked using parsed datetime values:

DEATHDATE < BIRTHDATE

Result:

Invalid records: 0

Conclusion: No patient has a death date earlier than their birth date.

Derived age

AGE is not a source column.

Decision: Derive age from BIRTHDATE when required rather than treating
it as an original source attribute.

1.8 Geographic Findings

COUNTY

Missing: 0

Decision: Retain.

FIPS

Missing: 1,575

Distinct non-missing values: 15

Decision: Retain and transform to an appropriate geographic-code type;
missing values remain representable as NULL.

ZIP

Findings:

ZIP = 0: 1,575

Non-zero ZIP values: 4,883

ZIP length:

1 digit: 1,575

4 digits: 4,883

Non-zero ZIP range: 1001–2861

ZIP = 0 and FIPS missing: 1,575

Conclusion: ZIP behaves as a geographic code rather than a mathematical
measurement.

Decision: Retain and transform to an appropriate character/string
representation. ZIP = 0 should not automatically be converted to SQL NULL
without confirming its intended source meaning.

LAT

Invalid values: 0

Decision: Retain.

LON

Invalid values: 0

Decision: Retain.

Detailed location fields

Column

Provisional decision

Reason

BIRTHPLACE

Exclude

Not required for current clinical patient scope

ADDRESS

Exclude

Detailed personal location information not required

CITY

Exclude

Current scope uses broader geographic information

STATE

Exclude

All records are Massachusetts

COUNTY

Retain

Complete broader geographic information

FIPS

Retain/transform

Standard geographic code

ZIP

Retain/transform

Geographic code

LAT

Retain

Valid geographic coordinate

LON

Retain

Valid geographic coordinate

These are current schema-scope decisions and can be revisited during final
normalization/schema review.

1.9 Financial Findings

HEALTHCARE_EXPENSES

Missing: 0

Negative values: 0

HEALTHCARE_COVERAGE

Missing: 0

Negative values: 0

Zero values: 137

INCOME

Missing: 0

Negative values: 0

Coverage versus expenses

Patients with HEALTHCARE_COVERAGE > HEALTHCARE_EXPENSES: 3,598

This is treated as an observed pattern, not automatically classified as
an error because no business rule has been established requiring coverage to
be less than expenses.

Decision

For the current core clinical database scope:

HEALTHCARE_EXPENSES → Exclude

HEALTHCARE_COVERAGE → Exclude

INCOME → Exclude

These fields remain available in the unchanged raw source and can be
reconsidered for future analytical/ML work.

1.10 PATIENTS Provisional Column Decisions

Retain

Id

FIRST

LAST

BIRTHDATE

DEATHDATE

MARITAL

RACE

ETHNICITY

GENDER

COUNTY

FIPS

ZIP

LAT

LON

Transform

BIRTHDATE → database DATE

DEATHDATE → nullable database DATE

FIPS → appropriate geographic-code representation

ZIP → appropriate character/string representation

Exclude from current processed clinical table

SSN

DRIVERS

PASSPORT

PREFIX

MIDDLE

SUFFIX

MAIDEN

BIRTHPLACE

ADDRESS

CITY

STATE

HEALTHCARE_EXPENSES

HEALTHCARE_COVERAGE

INCOME

Derived later

AGE → derive from BIRTHDATE when required.
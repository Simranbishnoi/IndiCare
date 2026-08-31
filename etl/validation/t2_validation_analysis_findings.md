# IndiCare – Clinical Data Validation Findings

This document records the pre-ETL data-quality and integrity validation checks
performed on the raw clinical CSV datasets before database loading.

The validation was performed using Python and Pandas to inspect:

- Dataset structure and schema
- Missing values
- Candidate keys
- Duplicate records
- Foreign-key referential integrity
- CODE–DESCRIPTION consistency
- Date consistency
- Relationships between clinical datasets

---

# 1. Conditions Dataset Analysis (`conditions.csv`)

## 1.1 Dataset Volume & Schema

- Total Records: 330,825 rows
- Total Attributes: 7 columns

### Columns

- START
- STOP
- PATIENT
- ENCOUNTER
- SYSTEM
- CODE
- DESCRIPTION

## 1.2 Entity Cardinality

- Unique Patients: 6,458
- Unique Encounters: 207,253
- Unique Condition Codes: 304
- Unique System Identifiers: 1

## 1.3 Missing Value Audit

| Column | Missing Count | Missing Percentage | Classification |
|---|---:|---:|---|
| START | 0 | 0.00% | Complete |
| STOP | 90,129 | 27.24% | Valid NULL |
| PATIENT | 0 | 0.00% | Complete |
| ENCOUNTER | 0 | 0.00% | Complete |
| SYSTEM | 0 | 0.00% | Complete |
| CODE | 0 | 0.00% | Complete |
| DESCRIPTION | 0 | 0.00% | Complete |

### Finding

The 90,129 missing STOP dates may represent ongoing or chronic conditions.
These records should be preserved rather than automatically treated as
errors.

## 1.4 Duplicate & Candidate Key Analysis

Candidate key tested:

`(ENCOUNTER, CODE)`

Results:

- Duplicate Rows: 0
- Duplicate Combinations: 0

### Conclusion

`(ENCOUNTER, CODE)` was found to be unique in the validated Conditions data.

## 1.5 Foreign-Key Referential Integrity

Tested relationship:

`CONDITIONS.ENCOUNTER → ENCOUNTERS.Id`

Results:

- Total Encounters rows: 280,533
- Matching Encounter IDs: 107,600
- Unmatched Condition rows: 159,197
- Unique unmatched Encounter IDs: 99,653

### Finding

159,197 condition records reference encounter IDs that are not present in
the Encounters table.

### ETL Directive

Do not automatically delete these records. They should be retained during
staging while the orphan encounter references are handled during ETL and
foreign-key constraint design.

## 1.6 CODE–DESCRIPTION Consistency

- Codes with multiple descriptions: 0
- Maximum descriptions for one code: 1

### Conclusion

Each Condition CODE maps to a single DESCRIPTION in the validated dataset.

---

# 2. Observations Dataset Analysis (`observations.csv`)

## 2.1 Dataset Schema

The Observations dataset contains 9 columns:

- DATE
- PATIENT
- ENCOUNTER
- CATEGORY
- CODE
- DESCRIPTION
- VALUE
- UNITS
- TYPE

## 2.2 Missing Value Audit

| Column | Missing Count | Finding |
|---|---:|---|
| ENCOUNTER | 121,444 | Missing encounter references |
| CATEGORY | 121,444 | Corresponds to rows with missing ENCOUNTER |
| CODE | 1 | Single missing observation code |
| TYPE | 1 | Single missing type descriptor |

## 2.3 Progressive Duplicate Key Investigation

| Stage | Key Tested | Duplicate Rows | Duplicate Combinations |
|---|---|---:|---:|
| Check 1 | ENCOUNTER + CODE + DATE | 48,405 | 23,320 |
| Check 2 | PATIENT + ENCOUNTER + CODE + DATE | 33,516 | 16,291 |
| Check 3 | PATIENT + ENCOUNTER + CODE + DATE + VALUE | 3,770 | 1,885 |
| Check 4 | Exact Full-Row Duplicates | 3,770 | 1,885 |
| Post-Deduplication | After removing exact duplicates | 0 | 0 |

### Finding

The remaining duplicate records were exact duplicate rows.

### ETL Directive

Exact duplicate rows can be removed using:

`drop_duplicates()`

This resolves the duplicate-key issue without losing unique observation
information.

## 2.4 CODE–DESCRIPTION Consistency

- Codes with multiple descriptions: 1
- Problematic CODE: `6299-2`

Descriptions found:

1. Urea nitrogen [Mass/volume] in Blood
2. Urea Nitrogen [Mass/volume] in Blood

### Finding

The difference is only capitalization.

### ETL Directive

Treat CODE as the stable identifier and standardize the DESCRIPTION text
during ETL.

---

# 3. Medications Dataset Analysis (`medications.csv`)

## 3.1 Foreign-Key Referential Integrity

Tested relationship:

`MEDICATIONS.ENCOUNTER → ENCOUNTERS.Id`

Results:

- Invalid Encounter references: 541,184
- Unique invalid Encounter IDs: 277,608

### Finding

A large number of medication records reference encounter IDs that are not
present in the Encounters table.

### ETL Directive

Do not automatically delete these medication records. Retain them during
staging while the orphan encounter references are investigated and handled
during ETL.

## 3.2 Candidate Key / Duplicate Analysis

Candidate key tested:

`(PATIENT, CODE, START, STOP)`

Results:

- Duplicate rows: 10
- Duplicate combinations: 5

### Finding

The duplicate medication records included different ENCOUNTER values.

This indicates that ENCOUNTER is important for distinguishing separate
medication events.

### Schema Implication

ENCOUNTER should be considered when defining the final relational key for
Medication records.

## 3.3 Missing STOP Values

- Missing STOP dates: 29,249

### Finding

A missing STOP date may represent an ongoing medication or an order without
a recorded termination date.

### ETL Directive

Preserve these values as NULL rather than assigning artificial terminal dates.

## 3.4 CODE–DESCRIPTION Consistency

- Codes with multiple descriptions: 14
- Maximum descriptions per code: 2

### Problematic Medication Codes

'''text
242969
243670
245314
309362
312961
314231
583214
855332
856987
1000126
1049221
1437975
1659149
1804799
# 4. Procedures Dataset Analysis (`procedures.csv`)

## 4.1 Dataset Volume & Schema

- Total Records: 541,434 rows
- Total Attributes: 10 columns

### Columns

- START
- STOP
- PATIENT
- ENCOUNTER
- SYSTEM
- CODE
- DESCRIPTION
- BASE_COST
- REASONCODE
- REASONDESCRIPTION

## 4.2 Entity Cardinality

- Unique Patients: 2,249
- Unique Encounters: 141,754
- Unique Procedure Codes: 368

## 4.3 Missing Value Audit

| Column | Missing Count |
|---|---:|
| START | 0 |
| STOP | 0 |
| PATIENT | 0 |
| ENCOUNTER | 0 |
| SYSTEM | 0 |
| CODE | 0 |
| DESCRIPTION | 0 |
| BASE_COST | 1 |
| REASONCODE | 305,389 |
| REASONDESCRIPTION | 305,389 |

### Finding

`BASE_COST` has 1 missing value.

`REASONCODE` and `REASONDESCRIPTION` both have 305,389 missing values.
These two fields are missing together in the validated records.

## 4.4 Candidate Key Analysis

Candidate key tested:

`(PATIENT, ENCOUNTER, CODE, START)`

Results:

- Duplicate key rows: 0
- Duplicate key combinations: 0

### Conclusion

No duplicate combinations were found using the tested candidate key
`(PATIENT, ENCOUNTER, CODE, START)`.

## 4.5 Exact Duplicate Analysis

The exact duplicate check was performed using all procedure columns.

Result:

- Exact duplicate rows: 0

### Conclusion

No completely identical Procedure records were found.

## 4.6 Foreign-Key Validation

The Procedure table was checked against the related Patients and Encounters
tables.

### PATIENT Reference

Tested relationship:

`PROCEDURES.PATIENT → PATIENTS.Id`

Result:

- Invalid PATIENT references: 0

### ENCOUNTER Reference

Tested relationship:

`PROCEDURES.ENCOUNTER → ENCOUNTERS.Id`

Result:

- Invalid ENCOUNTER references: 0

### Conclusion

The tested PATIENT and ENCOUNTER references in the Procedures dataset are
valid.

## 4.7 Date Consistency Check

The following condition was checked:

`STOP < START`

Result:

- Invalid date-order records: 1

Problematic record:

- CODE: `773996000`
- DESCRIPTION: `Transcatheter aortic valve implantation (procedure)`
- START: `2008-10-02 06:29:55+00:00`
- STOP: `2008-10-02 06:28:36+00:00`

### Finding

The STOP timestamp occurs before the START timestamp.

### ETL Directive

This record should be investigated before final database loading. It should
not be silently modified without a documented transformation rule.

## 4.8 CODE–DESCRIPTION Consistency

- Codes with multiple descriptions: 1
- Problematic CODE: `171207006`

Descriptions found:

1. `Depression screening (procedure)`
2. `Depressio`

### Finding

The second description appears to be incomplete.

This is not simply a capitalization difference.

### ETL Directive

Investigate the correct description before final database loading. Do not
automatically replace the value without documenting the source or
transformation rule.


# 5. Allergies Dataset Analysis (`allergies.csv`)

## 5.1 Missing Value Audit

| Column | Missing Count |
|---|---:|
| START | 0 |
| STOP | 3,978 |
| PATIENT | 0 |
| ENCOUNTER | 0 |
| CODE | 0 |
| SYSTEM | 0 |
| DESCRIPTION | 0 |
| TYPE | 0 |
| CATEGORY | 0 |
| REACTION1 | 2,324 |
| DESCRIPTION1 | 2,324 |
| SEVERITY1 | 2,324 |
| REACTION2 | 2,982 |
| DESCRIPTION2 | 2,982 |
| SEVERITY2 | 2,982 |

### Finding

There are 3,978 missing `STOP` dates.

The reaction-related fields are also missing for some records:

- `REACTION1`: 2,324
- `DESCRIPTION1`: 2,324
- `SEVERITY1`: 2,324
- `REACTION2`: 2,982
- `DESCRIPTION2`: 2,982
- `SEVERITY2`: 2,982

### ETL Directive

Missing values should be preserved as `NULL` where the corresponding
clinical information is not recorded.

Do not create artificial values for missing allergy end dates or reaction
information.

## 5.2 Candidate Key Analysis

Candidate key tested:

`(PATIENT, ENCOUNTER, CODE, START)`

Result:

- Duplicate candidate-key rows: 0

### Conclusion

No duplicate allergy records were found using the tested candidate key.

## 5.3 Exact Duplicate Analysis

The allergy records were checked for duplicate combinations using:

`PATIENT + ENCOUNTER + CODE + START`

Result:

- Duplicate rows: 0

### Conclusion

No duplicate allergy records were identified using the tested key.

## 5.4 PATIENT Foreign-Key Validation

Tested relationship:

`ALLERGIES.PATIENT → PATIENTS.Id`

Result:

- Invalid PATIENT references: 0

### Conclusion

All tested Allergy PATIENT references are valid.

## 5.5 ENCOUNTER Foreign-Key Validation

Tested relationship:

`ALLERGIES.ENCOUNTER → ENCOUNTERS.Id`

Results:

- Invalid Encounter references: 1,871
- Unique invalid Encounter IDs: 447

### Finding

1,871 Allergy records reference 447 encounter IDs that are not present in the
Encounters dataset.

### Example

Some records contain valid Patient IDs but their associated Encounter IDs
are absent from `encounters.csv`.

### ETL Directive

Do not automatically delete these Allergy records.

Retain the records during staging and handle the orphan Encounter references
during the ETL and final foreign-key constraint process.

## 5.6 CODE–DESCRIPTION Consistency

Result:

- Codes with multiple descriptions: 0

### Conclusion

Each Allergy CODE maps to a single DESCRIPTION in the validated dataset.

## 5.7 Date Consistency Check

The following condition was checked:

`STOP < START`

Result:

- Invalid date-order records: 0

### Conclusion

No Allergy records were found where a non-null STOP date occurs before the
START date.

## 5.8 Overall Allergy Validation Conclusion

The Allergy dataset has:

- No missing PATIENT values
- No missing ENCOUNTER values
- No missing CODE values
- No duplicate candidate-key combinations
- No invalid PATIENT references
- No invalid date-order records
- 1,871 invalid ENCOUNTER references
- 3,978 missing STOP dates
- Missing reaction and severity information in some records

The main ETL concern is the set of orphan ENCOUNTER references. These records
should be retained during staging rather than automatically deleted.
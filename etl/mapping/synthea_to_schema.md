# OBSERVATIONS

## 1. Source

Source file:

`data/raw/synthea/observations.csv`

Source columns:

- DATE
- PATIENT
- ENCOUNTER
- CATEGORY
- CODE
- DESCRIPTION
- VALUE
- UNITS
- TYPE

---

## 2. Target table

Target:

`OBSERVATIONS`

Reference table:

`ObservationCode`

---

## 3. Column mapping

| Synthea column | Target | Transformation / rule |
|---|---|---|
| DATE | observation_date | Convert source date/time to database-compatible DATE/TIMESTAMP according to final schema |
| PATIENT | patient_id | Map to `PATIENTS` primary key |
| ENCOUNTER | encounter_id | Map to `ENCOUNTERS` primary key; source can be NULL |
| CATEGORY | category | Preserve value; source is NULL when ENCOUNTER is NULL |
| CODE | ObservationCode.code | Map observation code to reference table |
| DESCRIPTION | ObservationCode.description | Preserve/standardize description |
| VALUE | value | Preserve original value |
| UNITS | units | Preserve original value; NULL allowed |
| TYPE | type | Preserve original value |

---

## 4. Validation findings that affect ETL

### Missing values

- `ENCOUNTER`: 121,444 missing
- `CATEGORY`: 121,444 missing
- `CODE`: 1 missing
- `TYPE`: 1 missing

The missing `ENCOUNTER` and `CATEGORY` values correspond to the same records.

Do not invent encounter IDs or category values.

Preserve valid missing values as NULL where the final schema permits them.

---

## 5. Duplicate handling

Validation identified duplicates at several levels.

After checking progressively:

1. `ENCOUNTER + CODE + DATE`
2. `PATIENT + ENCOUNTER + CODE + DATE`
3. `PATIENT + ENCOUNTER + CODE + DATE + VALUE`
4. Exact full-row duplicate

The remaining exact duplicate records were:

- 3,770 duplicate rows
- 1,885 duplicate combinations

ETL rule:

**Remove exact duplicate rows only.**

Do not remove records merely because they share the same patient, encounter, code, or date.

Use deterministic exact-row deduplication, equivalent to:

`drop_duplicates()`

---

## 6. Code/description handling

Validation found that code `6299-2` has two descriptions differing only by capitalization.

ETL rule:

- Treat `CODE` as the stable identifier.
- Standardize the description consistently during transformation.
- Do not create separate reference-code records solely because of capitalization differences.

The final standardized description must be documented in the transformation logic.

---

## 7. Reference table

`ObservationCode`

Purpose:

Store unique observation codes and their descriptions separately from the observation event records.

Expected logical structure:

| Column | Role |
|---|---|
| code | Primary key |
| description | Code description |

Populate the reference table from the cleaned/transformed observation data using unique codes.

---

## 8. Patient relationship

`OBSERVATIONS.PATIENT` maps to:

`PATIENTS.Id`

Patient references should be validated before final loading.

Do not silently replace invalid patient IDs.

---

## 9. Encounter relationship

`OBSERVATIONS.ENCOUNTER` maps to:

`ENCOUNTERS.Id`

Because `ENCOUNTER` is missing for 121,444 records:

- preserve NULL encounter references where allowed;
- do not invent an encounter ID;
- do not automatically delete these observations;
- validate non-null encounter IDs against `ENCOUNTERS` before final loading.

---

## 10. ETL rules

1. Read `observations.csv` from `data/raw/synthea/`.
2. Leave the raw CSV unchanged.
3. Remove exact duplicate rows only.
4. Preserve valid NULL values.
5. Standardize the `6299-2` description consistently.
6. Create/populate `ObservationCode` from unique observation codes.
7. Map patient IDs to `PATIENTS`.
8. Map encounter IDs to `ENCOUNTERS`.
9. Preserve observation values and units.
10. Validate the transformed data before loading into PostgreSQL.

---

## 11. Post-transformation validation

Before final loading, verify:

- no exact duplicate observation rows;
- `CODE` is not unexpectedly NULL;
- `PATIENT` references are valid;
- non-null `ENCOUNTER` references are valid;
- NULL `ENCOUNTER` values are preserved;
- `VALUE`, `UNITS`, and `TYPE` are not unintentionally changed;
- code/description consistency is maintained;
- `ObservationCode.code` contains unique codes.

# MEDICATIONS

## 1. Source

Source file:

`data/raw/synthea/medications.csv`

The source contains medication event information associated with patients and encounters.

---

## 2. Target table

Target:

`MEDICATIONS`

Reference table:

`MedicationCode`

---

## 3. Column mapping

| Synthea column | Target | Transformation / rule |
|---|---|---|
| START | start | Convert source date/time to database-compatible DATE/TIMESTAMP according to final schema |
| STOP | stop | Convert source date/time; preserve missing values as NULL |
| PATIENT | patient_id | Map to `PATIENTS` primary key |
| ENCOUNTER | encounter_id | Map to `ENCOUNTERS` primary key |
| CODE | MedicationCode.code | Map medication code to reference table |
| DESCRIPTION | MedicationCode.description | Preserve/standardize description |
| BASE_COST | base_cost | Preserve numeric value |
| PAYER_COVERAGE | payer_coverage | Preserve numeric value |
| DISPENSES | dispenses | Preserve numeric value |
| TOTALCOST | total_cost | Preserve numeric value |
| REASONCODE | reason_code | Preserve value; NULL allowed |
| REASONDESCRIPTION | reason_description | Preserve value; NULL allowed |

---

## 4. Missing values

Validation found:

- `STOP`: 29,249 missing

ETL rule:

- Preserve missing `STOP` values as NULL.
- Do not create artificial medication end dates.
- Do not assume that a missing STOP means a particular clinical status.

Other missing-value handling must follow the source data and final relational schema.

---

## 5. Encounter foreign-key validation

Validation found:

- Invalid encounter references: 541,184
- Unique invalid encounter IDs: 277,608

ETL rule:

- Do not automatically delete these medication records.
- Do not invent replacement encounter IDs.
- Retain the records during staging/cleaning.
- Investigate and handle orphan encounter references before final database loading.
- The final FK constraint must only be applied according to the agreed orphan-handling strategy.

---

## 6. Duplicate handling

Validation checked the candidate key:

`PATIENT + CODE + START + STOP`

Results:

- 10 duplicate rows
- 5 duplicate combinations

The duplicate records include different `ENCOUNTER` values.

Therefore:

**ENCOUNTER is important for distinguishing medication events.**

ETL rule:

- Do not deduplicate medications using only `PATIENT + CODE + START + STOP`.
- Preserve records that represent different encounters.
- Do not remove medication records solely because patient, code, start, and stop values are identical unless they are confirmed to be exact duplicates according to the agreed ETL rule.

---

## 7. Medication code/description consistency

Validation found 14 medication codes with multiple descriptions:

- 242969
- 243670
- 245314
- 309362
- 312961
- 314231
- 583214
- 855332
- 856987
- 1000126
- 1049221
- 1437975
- 1659149
- 1804799

ETL rule:

- Do not silently choose one description.
- Do not automatically overwrite the source descriptions.
- Investigate/document the correct handling before final population of `MedicationCode`.
- Preserve the source information during staging.

---

## 8. Reference table

`MedicationCode`

Purpose:

Store medication codes and their descriptions separately from medication event records.

Expected logical structure:

| Column | Role |
|---|---|
| code | Primary key |
| description | Medication description |

The exact final structure must follow the approved relational schema.

---

## 9. Patient relationship

`MEDICATIONS.PATIENT` maps to:

`PATIENTS.Id`

Patient IDs must be validated before final loading.

Do not silently replace invalid patient IDs.

---

## 10. Encounter relationship

`MEDICATIONS.ENCOUNTER` maps to:

`ENCOUNTERS.Id`

Because validation identified a large number of invalid encounter references:

- retain the source records during staging;
- do not invent encounter IDs;
- do not silently replace IDs;
- resolve the orphan-reference strategy before applying the final FK constraint.

---

## 11. ETL rules

1. Read `medications.csv` from `data/raw/synthea/`.
2. Leave the raw CSV unchanged.
3. Convert date/time fields according to the final schema.
4. Preserve missing `STOP` values as NULL.
5. Preserve medication event records during staging.
6. Do not deduplicate using only `PATIENT + CODE + START + STOP`.
7. Preserve `ENCOUNTER` because it distinguishes medication events.
8. Investigate the 14 codes with multiple descriptions.
9. Create/populate `MedicationCode` according to the approved code/reference-table design.
10. Validate patient and encounter references.
11. Resolve orphan encounter handling before final database loading.
12. Validate the transformed data before loading into PostgreSQL.

---

## 12. Post-transformation validation

Before final loading, verify:

- medication date fields have the correct database format;
- missing `STOP` values remain NULL;
- medication records have not been incorrectly deleted;
- patient references are valid;
- encounter references are either valid or explicitly handled by the agreed orphan strategy;
- medication codes are represented correctly in `MedicationCode`;
- the 14 codes with multiple descriptions have documented handling;
- numeric fields remain numeric;
- no unintended data changes occurred during transformation.

# PROCEDURES

## 1. Source

Source file:

`data/raw/synthea/procedures.csv`

Source columns:

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

---

## 2. Target table

Target:

`PROCEDURES`

Reference table:

`ProcedureCode`

---

## 3. Column mapping

| Synthea column | Target | Transformation / rule |
|---|---|---|
| START | start | Convert source date/time to database-compatible DATE/TIMESTAMP according to final schema |
| STOP | stop | Convert source date/time; preserve NULL where applicable |
| PATIENT | patient_id | Map to `PATIENTS` primary key |
| ENCOUNTER | encounter_id | Map to `ENCOUNTERS` primary key |
| SYSTEM | system | Preserve source value |
| CODE | ProcedureCode.code | Map procedure code to reference table |
| DESCRIPTION | ProcedureCode.description | Preserve source description |
| BASE_COST | base_cost | Preserve numeric value; handle the single missing value according to schema rules |
| REASONCODE | reason_code | Preserve value; NULL allowed |
| REASONDESCRIPTION | reason_description | Preserve value; NULL allowed |

---

## 4. Missing values

Validation found:

- `BASE_COST`: 1 missing
- `REASONCODE`: 305,389 missing
- `REASONDESCRIPTION`: 305,389 missing

The missing reason fields occur together.

ETL rule:

- Preserve valid missing values as NULL.
- Do not invent reason codes or descriptions.
- Do not replace missing clinical information with artificial values.

---

## 5. Primary/candidate key

Validation found the following candidate key to be unique:

`PATIENT + ENCOUNTER + CODE + START`

Results:

- Duplicate key rows: 0
- Duplicate key combinations: 0
- Exact duplicate rows: 0

Therefore, this combination can be used as the validated candidate key for identifying procedure events.

The final primary-key decision must follow the approved relational schema.

---

## 6. Patient foreign key

`PROCEDURES.PATIENT` maps to:

`PATIENTS.Id`

Validation confirmed patient references are valid.

ETL rule:

- Preserve patient IDs.
- Validate the relationship before final loading.
- Do not modify valid patient IDs.

---

## 7. Encounter foreign key

`PROCEDURES.ENCOUNTER` maps to:

`ENCOUNTERS.Id`

Validation confirmed encounter references are valid.

ETL rule:

- Preserve encounter IDs.
- Validate the relationship before final loading.
- Do not modify valid encounter IDs.

---

## 8. Date validation

Validation found one record where:

`STOP < START`

Record:

- CODE: `773996000`
- DESCRIPTION: `Transcatheter aortic valve implantation (procedure)`
- START: `2008-10-02 06:29:55+00:00`
- STOP: `2008-10-02 06:28:36+00:00`

ETL rule:

- Do not silently change START or STOP.
- Do not automatically swap the dates.
- Flag this record for investigation.
- Document the final decision before final database loading.

---

## 9. Procedure code/description consistency

Validation found code:

`171207006`

with two descriptions:

- `Depression screening (procedure)`
- `Depressio`

The second description appears incomplete.

ETL rule:

- Do not silently replace the description.
- Investigate/document the correct handling.
- Preserve the source information during staging.
- Apply any correction only through a documented transformation rule.

---

## 10. Reference table

`ProcedureCode`

Purpose:

Store unique procedure codes and their descriptions separately from procedure event records.

Expected logical structure:

| Column | Role |
|---|---|
| code | Primary key |
| description | Procedure description |

The exact final structure must follow the approved relational schema.

---

## 11. ETL rules

1. Read `procedures.csv` from `data/raw/synthea/`.
2. Leave the raw CSV unchanged.
3. Convert date/time fields according to the final schema.
4. Preserve NULL values.
5. Preserve the validated procedure event uniqueness.
6. Validate patient references.
7. Validate encounter references.
8. Create/populate `ProcedureCode` according to the approved reference-table design.
9. Investigate the `STOP < START` record before final loading.
10. Investigate the inconsistent description for code `171207006`.
11. Do not silently modify questionable source data.
12. Validate transformed data before loading into PostgreSQL.

---

## 12. Post-transformation validation

Before final loading, verify:

- no unintended duplicate procedure events;
- patient references are valid;
- encounter references are valid;
- date fields have the correct database format;
- the `STOP < START` record has documented handling;
- code `171207006` has documented description handling;
- missing reason information remains NULL;
- `BASE_COST` is handled according to the final schema;
- `ProcedureCode.code` contains unique procedure codes;
- no unintended source data changes occurred.

# ALLERGIES

## 1. Source

Source file:

`data/raw/synthea/allergies.csv`

Source columns:

- START
- STOP
- PATIENT
- ENCOUNTER
- CODE
- SYSTEM
- DESCRIPTION
- TYPE
- CATEGORY
- REACTION1
- DESCRIPTION1
- SEVERITY1
- REACTION2
- DESCRIPTION2
- SEVERITY2

---

## 2. Target table

Target:

`ALLERGIES`

Reference table:

`AllergyCode`

---

## 3. Column mapping

| Synthea column | Target | Transformation / rule |
|---|---|---|
| START | start | Convert source date/time to database-compatible DATE/TIMESTAMP according to final schema |
| STOP | stop | Convert source date/time; preserve NULL |
| PATIENT | patient_id | Map to `PATIENTS` primary key |
| ENCOUNTER | encounter_id | Map to `ENCOUNTERS` primary key |
| CODE | AllergyCode.code | Map allergy code to reference table |
| SYSTEM | system | Preserve source value |
| DESCRIPTION | AllergyCode.description | Preserve source description |
| TYPE | type | Preserve source value |
| CATEGORY | category | Preserve source value |
| REACTION1 | reaction1 | Preserve value; NULL allowed |
| DESCRIPTION1 | reaction_description1 | Preserve value; NULL allowed |
| SEVERITY1 | severity1 | Preserve value; NULL allowed |
| REACTION2 | reaction2 | Preserve value; NULL allowed |
| DESCRIPTION2 | reaction_description2 | Preserve value; NULL allowed |
| SEVERITY2 | severity2 | Preserve value; NULL allowed |

---

## 4. Missing values

Validation found:

- `STOP`: 3,978 missing
- `REACTION1`: 2,324 missing
- `DESCRIPTION1`: 2,324 missing
- `SEVERITY1`: 2,324 missing
- `REACTION2`: 2,982 missing
- `DESCRIPTION2`: 2,982 missing
- `SEVERITY2`: 2,982 missing

ETL rule:

- Preserve missing values as NULL.
- Do not invent allergy reactions, descriptions, or severity.
- Do not create artificial STOP dates.

---

## 5. Candidate key

Validation checked:

`PATIENT + ENCOUNTER + CODE + START`

Results:

- Duplicate rows: 0
- Duplicate combinations: 0

Therefore, this combination was validated as unique in the source data.

The final primary-key decision must follow the approved relational schema.

---

## 6. Patient foreign key

`ALLERGIES.PATIENT` maps to:

`PATIENTS.Id`

Validation found:

- Invalid patient references: 0

ETL rule:

- Preserve patient IDs.
- Validate the relationship before final loading.
- Do not modify valid patient IDs.

---

## 7. Encounter foreign key

`ALLERGIES.ENCOUNTER` maps to:

`ENCOUNTERS.Id`

Validation found:

- Invalid encounter references: 1,871
- Unique invalid encounter IDs: 447

ETL rule:

- Do not automatically delete allergy records.
- Do not invent replacement encounter IDs.
- Retain records during staging.
- Investigate and resolve the orphan encounter strategy before final database loading.
- Apply the final FK constraint only according to the agreed orphan-handling strategy.

---

## 8. Allergy code/description consistency

Validation found:

- No code has multiple descriptions.

Therefore:

- `CODE` can be treated as the stable allergy-code identifier.
- The description can be associated with the corresponding code in `AllergyCode`.
- No description correction is currently required based on validation findings.

---

## 9. Date validation

Validation found:

- No records where `STOP < START`.

ETL rule:

- Convert date/time fields according to the final schema.
- Preserve valid NULL STOP values.
- No date correction is currently required.

---

## 10. Reference table

`AllergyCode`

Purpose:

Store unique allergy codes and their descriptions separately from allergy event records.

Expected logical structure:

| Column | Role |
|---|---|
| code | Primary key |
| description | Allergy description |

The exact final structure must follow the approved relational schema.

---

## 11. ETL rules

1. Read `allergies.csv` from `data/raw/synthea/`.
2. Leave the raw CSV unchanged.
3. Convert date/time fields according to the final schema.
4. Preserve missing STOP values as NULL.
5. Preserve missing reaction fields as NULL.
6. Preserve the validated allergy event uniqueness.
7. Validate patient references.
8. Validate encounter references.
9. Create/populate `AllergyCode` according to the approved reference-table design.
10. Do not invent missing clinical information.
11. Resolve orphan encounter handling before final database loading.
12. Validate transformed data before loading into PostgreSQL.

---

## 12. Post-transformation validation

Before final loading, verify:

- no unintended duplicate allergy events;
- patient references are valid;
- non-null encounter references are either valid or explicitly handled by the agreed orphan strategy;
- missing STOP values remain NULL;
- missing reaction information remains NULL;
- allergy codes are represented correctly in `AllergyCode`;
- code/description consistency is maintained;
- date fields have the correct database format;
- no unintended source data changes occurred.
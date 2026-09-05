-- ============================================================
-- IndiCare Database Schema
-- Based on:
--   1. Handwritten relational design
--   2. ETL validation findings
--   3. Transformed Synthea data
--
-- Synthea column names are preserved.
-- ============================================================


-- ============================================================
-- 1. CODE REFERENCE TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS EncounterCode (
    CODE VARCHAR(50) PRIMARY KEY,
    DESCRIPTION TEXT
);


CREATE TABLE IF NOT EXISTS ConditionCode (
    CODE VARCHAR(50),
    DESCRIPTION TEXT,
    PRIMARY KEY (CODE, DESCRIPTION)
);


CREATE TABLE IF NOT EXISTS ObservationCode (
    CODE VARCHAR(50),
    DESCRIPTION TEXT,
    PRIMARY KEY (CODE, DESCRIPTION)
);


CREATE TABLE IF NOT EXISTS MedicationCode (
    CODE VARCHAR(50),
    DESCRIPTION TEXT,
    PRIMARY KEY (CODE, DESCRIPTION)
);


CREATE TABLE IF NOT EXISTS ProcedureCode (
    CODE VARCHAR(50),
    DESCRIPTION TEXT,
    PRIMARY KEY (CODE, DESCRIPTION)
);


CREATE TABLE IF NOT EXISTS AllergiesCode (
    CODE VARCHAR(50),
    DESCRIPTION TEXT,
    PRIMARY KEY (CODE, DESCRIPTION)
);


-- ============================================================
-- 2. PATIENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS Patients (
    Id VARCHAR(100) PRIMARY KEY,
    BIRTHDATE DATE NOT NULL,
    DEATHDATE DATE,
    MARITAL VARCHAR(10),
    RACE VARCHAR(100),
    ETHNICITY VARCHAR(100),
    GENDER VARCHAR(20),
    COUNTY VARCHAR(100),
    FIPS VARCHAR(20),
    ZIP VARCHAR(20),
    LAT NUMERIC(10, 6),
    LON NUMERIC(10, 6),
    FIRST VARCHAR(100),
    LAST VARCHAR(100)
);


-- ============================================================
-- 3. ENCOUNTERS
-- ============================================================

CREATE TABLE IF NOT EXISTS Encounters (
    Id VARCHAR(100) PRIMARY KEY,
    PATIENT VARCHAR(100) NOT NULL,
    START TIMESTAMPTZ NOT NULL,
    STOP TIMESTAMPTZ,
    ENCOUNTERCLASS VARCHAR(50),
    CODE VARCHAR(50),
    DESCRIPTION TEXT,

    CONSTRAINT fk_encounters_patient
        FOREIGN KEY (PATIENT)
        REFERENCES Patients(Id),

    CONSTRAINT fk_encounters_code
        FOREIGN KEY (CODE)
        REFERENCES EncounterCode(CODE)
);


-- ============================================================
-- 4. CONDITIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS Conditions (
    START TIMESTAMPTZ NOT NULL,
    STOP TIMESTAMPTZ,
    PATIENT VARCHAR(100) NOT NULL,
    ENCOUNTER VARCHAR(100) NOT NULL,
    CODE VARCHAR(50) NOT NULL,
    DESCRIPTION TEXT,

    CONSTRAINT pk_conditions
        PRIMARY KEY (ENCOUNTER, CODE),

    CONSTRAINT fk_conditions_patient
        FOREIGN KEY (PATIENT)
        REFERENCES Patients(Id),

    CONSTRAINT fk_conditions_encounter
        FOREIGN KEY (ENCOUNTER)
        REFERENCES Encounters(Id),

    CONSTRAINT fk_conditions_code
        FOREIGN KEY (CODE, DESCRIPTION)
        REFERENCES ConditionCode(CODE, DESCRIPTION)
);


-- ============================================================
-- 5. OBSERVATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS Observations (
    OBSERVATION_ID BIGSERIAL PRIMARY KEY,
    DATE TIMESTAMPTZ NOT NULL,
    PATIENT VARCHAR(100),
    ENCOUNTER VARCHAR(100),
    CATEGORY VARCHAR(100),
    CODE VARCHAR(50),
    DESCRIPTION TEXT,
    VALUE TEXT,
    UNITS VARCHAR(100),
    TYPE VARCHAR(100),

    CONSTRAINT fk_observations_patient
        FOREIGN KEY (PATIENT)
        REFERENCES Patients(Id),

    CONSTRAINT fk_observations_encounter
        FOREIGN KEY (ENCOUNTER)
        REFERENCES Encounters(Id),

    CONSTRAINT fk_observations_code
        FOREIGN KEY (CODE, DESCRIPTION)
        REFERENCES ObservationCode(CODE, DESCRIPTION)
);


-- ============================================================
-- 6. MEDICATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS Medications (
    MEDICATION_ID BIGSERIAL PRIMARY KEY,
    START TIMESTAMPTZ NOT NULL,
    STOP TIMESTAMPTZ,
    PATIENT VARCHAR(100) NOT NULL,
    ENCOUNTER VARCHAR(100),
    CODE VARCHAR(50) NOT NULL,
    DESCRIPTION TEXT,
    BASE_COST NUMERIC(14, 2),
    PAYER_COVERAGE NUMERIC(14, 2),
    DISPENSES NUMERIC(14, 2),
    TOTALCOST NUMERIC(14, 2),
    REASONCODE VARCHAR(50),
    REASONDESCRIPTION TEXT,

    CONSTRAINT fk_medications_patient
        FOREIGN KEY (PATIENT)
        REFERENCES Patients(Id),

    CONSTRAINT fk_medications_encounter
        FOREIGN KEY (ENCOUNTER)
        REFERENCES Encounters(Id),

    CONSTRAINT fk_medications_code
        FOREIGN KEY (CODE, DESCRIPTION)
        REFERENCES MedicationCode(CODE, DESCRIPTION)
);


-- ============================================================
-- 7. PROCEDURES
-- ============================================================

CREATE TABLE IF NOT EXISTS Procedures (
    START TIMESTAMPTZ NOT NULL,
    STOP TIMESTAMPTZ,
    PATIENT VARCHAR(100) NOT NULL,
    ENCOUNTER VARCHAR(100) NOT NULL,
    SYSTEM VARCHAR(100),
    CODE VARCHAR(50) NOT NULL,
    DESCRIPTION TEXT,
    BASE_COST NUMERIC(14, 2),
    REASONCODE VARCHAR(50),
    REASONDESCRIPTION TEXT,

    CONSTRAINT pk_procedures
        PRIMARY KEY (PATIENT, ENCOUNTER, CODE, START),

    CONSTRAINT fk_procedures_patient
        FOREIGN KEY (PATIENT)
        REFERENCES Patients(Id),

    CONSTRAINT fk_procedures_encounter
        FOREIGN KEY (ENCOUNTER)
        REFERENCES Encounters(Id),

    CONSTRAINT fk_procedures_code
        FOREIGN KEY (CODE, DESCRIPTION)
        REFERENCES ProcedureCode(CODE, DESCRIPTION)
);


-- ============================================================
-- 8. ALLERGIES
-- ============================================================

CREATE TABLE IF NOT EXISTS Allergies (
    START TIMESTAMPTZ NOT NULL,
    STOP TIMESTAMPTZ,
    PATIENT VARCHAR(100) NOT NULL,
    ENCOUNTER VARCHAR(100) NOT NULL,
    CODE VARCHAR(50) NOT NULL,
    SYSTEM VARCHAR(100),
    DESCRIPTION TEXT,
    TYPE VARCHAR(100),
    CATEGORY VARCHAR(100),
    REACTION1 VARCHAR(100),
    DESCRIPTION1 TEXT,
    SEVERITY1 VARCHAR(100),
    REACTION2 VARCHAR(100),
    DESCRIPTION2 TEXT,
    SEVERITY2 VARCHAR(100),

    CONSTRAINT pk_allergies
        PRIMARY KEY (PATIENT, ENCOUNTER, CODE, START),

    CONSTRAINT fk_allergies_patient
        FOREIGN KEY (PATIENT)
        REFERENCES Patients(Id),

    CONSTRAINT fk_allergies_encounter
        FOREIGN KEY (ENCOUNTER)
        REFERENCES Encounters(Id),

    CONSTRAINT fk_allergies_code
        FOREIGN KEY (CODE, DESCRIPTION)
        REFERENCES AllergiesCode(CODE, DESCRIPTION)
);


-- ============================================================
-- 9. CAREPLANS
-- ============================================================

CREATE TABLE IF NOT EXISTS Careplans (
    Id VARCHAR(100) PRIMARY KEY,
    PATIENT VARCHAR(100) NOT NULL,
    ENCOUNTER VARCHAR(100),
    START TIMESTAMPTZ,
    CODE VARCHAR(50),

    CONSTRAINT fk_careplans_patient
        FOREIGN KEY (PATIENT)
        REFERENCES Patients(Id),

    CONSTRAINT fk_careplans_encounter
        FOREIGN KEY (ENCOUNTER)
        REFERENCES Encounters(Id)
);
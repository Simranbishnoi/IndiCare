-- IndiCare PostgreSQL DDL: tables.sql
-- Contains Staging Tables and Normalized Final Relational Tables

CREATE SCHEMA IF NOT EXISTS indicare;

-- ============================================================
-- 1. STAGING TABLES (For raw/processed CSV ingestion)
-- ============================================================

CREATE TABLE IF NOT EXISTS indicare.stg_patients (
    id VARCHAR(64),
    first VARCHAR(100),
    last VARCHAR(100),
    birthdate DATE,
    deathdate DATE,
    marital VARCHAR(10),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    gender VARCHAR(10),
    county VARCHAR(100),
    fips VARCHAR(20),
    zip VARCHAR(20),
    lat NUMERIC(10, 6),
    lon NUMERIC(10, 6)
);

CREATE TABLE IF NOT EXISTS indicare.stg_encounters (
    id VARCHAR(64),
    start_time TIMESTAMP,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64),
    organization VARCHAR(64),
    provider VARCHAR(64),
    payer VARCHAR(64),
    encounterclass VARCHAR(50),
    code VARCHAR(50),
    reasoncode VARCHAR(50),
    reasondescription TEXT
);

CREATE TABLE IF NOT EXISTS indicare.stg_careplans (
    id VARCHAR(64),
    start_time TIMESTAMP,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64),
    encounter_id VARCHAR(64),
    code VARCHAR(50),
    description TEXT,
    reasoncode VARCHAR(50),
    reasondescription TEXT
);

CREATE TABLE IF NOT EXISTS indicare.stg_conditions (
    start_date DATE,
    stop_date DATE,
    patient_id VARCHAR(64),
    encounter_id VARCHAR(64),
    system VARCHAR(100),
    code VARCHAR(50),
    description TEXT
);

CREATE TABLE IF NOT EXISTS indicare.stg_observations (
    obs_date TIMESTAMP,
    patient_id VARCHAR(64),
    encounter_id VARCHAR(64),
    category VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    value TEXT,
    units VARCHAR(50),
    obs_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS indicare.stg_medications (
    start_time TIMESTAMP,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64),
    payer_id VARCHAR(64),
    encounter_id VARCHAR(64),
    code VARCHAR(50),
    description TEXT,
    base_cost NUMERIC(12, 2),
    payer_coverage NUMERIC(12, 2),
    dispenses INT,
    total_cost NUMERIC(12, 2),
    reasoncode VARCHAR(50),
    reasondescription TEXT
);

CREATE TABLE IF NOT EXISTS indicare.stg_procedures (
    start_time TIMESTAMP,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64),
    encounter_id VARCHAR(64),
    system VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    base_cost NUMERIC(12, 2),
    reasoncode VARCHAR(50),
    reasondescription TEXT
);

CREATE TABLE IF NOT EXISTS indicare.stg_allergies (
    start_date DATE,
    stop_date DATE,
    patient_id VARCHAR(64),
    encounter_id VARCHAR(64),
    code VARCHAR(50),
    system VARCHAR(100),
    description TEXT,
    type VARCHAR(50),
    category VARCHAR(50),
    reaction1 VARCHAR(100),
    description1 TEXT,
    severity1 VARCHAR(50),
    reaction2 VARCHAR(100),
    description2 TEXT,
    severity2 VARCHAR(50)
);

-- ============================================================
-- 2. FINAL RELATIONAL TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS indicare.patients (
    patient_id VARCHAR(64) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    death_date DATE,
    marital_status VARCHAR(10),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    gender VARCHAR(10),
    county VARCHAR(100),
    fips VARCHAR(20),
    zip VARCHAR(20),
    lat NUMERIC(10, 6),
    lon NUMERIC(10, 6)
);

CREATE TABLE IF NOT EXISTS indicare.encounters (
    encounter_id VARCHAR(64) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64) NOT NULL,
    organization_id VARCHAR(64),
    provider_id VARCHAR(64),
    payer_id VARCHAR(64),
    encounter_class VARCHAR(50),
    code VARCHAR(50),
    reason_code VARCHAR(50),
    reason_description TEXT
);

CREATE TABLE IF NOT EXISTS indicare.careplans (
    careplan_id VARCHAR(64) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64) NOT NULL,
    encounter_id VARCHAR(64),
    code VARCHAR(50),
    description TEXT,
    reason_code VARCHAR(50),
    reason_description TEXT
);

CREATE TABLE IF NOT EXISTS indicare.conditions (
    condition_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    start_date DATE NOT NULL,
    stop_date DATE,
    patient_id VARCHAR(64) NOT NULL,
    encounter_id VARCHAR(64),
    system VARCHAR(100),
    code VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS indicare.observations (
    observation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    obs_date TIMESTAMP NOT NULL,
    patient_id VARCHAR(64) NOT NULL,
    encounter_id VARCHAR(64),
    category VARCHAR(100),
    code VARCHAR(50) NOT NULL,
    description TEXT,
    value TEXT,
    units VARCHAR(50),
    obs_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS indicare.medications (
    medication_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64) NOT NULL,
    payer_id VARCHAR(64),
    encounter_id VARCHAR(64),
    code VARCHAR(50) NOT NULL,
    description TEXT,
    base_cost NUMERIC(12, 2),
    payer_coverage NUMERIC(12, 2),
    dispenses INT,
    total_cost NUMERIC(12, 2),
    reason_code VARCHAR(50),
    reason_description TEXT
);

CREATE TABLE IF NOT EXISTS indicare.procedures (
    procedure_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP,
    patient_id VARCHAR(64) NOT NULL,
    encounter_id VARCHAR(64),
    system VARCHAR(100),
    code VARCHAR(50) NOT NULL,
    description TEXT,
    base_cost NUMERIC(12, 2),
    reason_code VARCHAR(50),
    reason_description TEXT
);

CREATE TABLE IF NOT EXISTS indicare.allergies (
    allergy_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    start_date DATE NOT NULL,
    stop_date DATE,
    patient_id VARCHAR(64) NOT NULL,
    encounter_id VARCHAR(64),
    code VARCHAR(50) NOT NULL,
    system VARCHAR(100),
    description TEXT,
    type VARCHAR(50),
    category VARCHAR(50),
    reaction1 VARCHAR(100),
    description1 TEXT,
    severity1 VARCHAR(50),
    reaction2 VARCHAR(100),
    description2 TEXT,
    severity2 VARCHAR(50)
);
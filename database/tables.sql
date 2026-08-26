
-- IndiCare
-- PostgreSQL
-- tables.sql

-- CODE / LOOKUP TABLES

CREATE TABLE indicare.encounter_code (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE indicare.condition_code (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE indicare.observation_code (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE indicare.medication_code (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE indicare.procedure_code (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE indicare.allergy_code (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

-- PATIENTS

CREATE TABLE indicare.patients (
    patient_id UUID PRIMARY KEY,
    birth_date DATE,
    gender VARCHAR(20),
    race VARCHAR(100),
    ethnicity VARCHAR(100)
);

-- ENCOUNTERS

CREATE TABLE indicare.encounters (
    encounter_id UUID PRIMARY KEY,
    patient_id UUID NOT NULL,
    start_time TIMESTAMP,
    stop_time TIMESTAMP,
    encounter_class VARCHAR(50),
    code VARCHAR(50)
);


-- CONDITIONS

CREATE TABLE indicare.conditions (
    encounter_id UUID NOT NULL,
    code VARCHAR(50) NOT NULL,
    start_date DATE,
    stop_date DATE
);

-- OBSERVATIONS

CREATE TABLE indicare.observations (
    encounter_id UUID NOT NULL,
    observation_date DATE,
    code VARCHAR(50) NOT NULL,
    value TEXT,
    units VARCHAR(50),
    observation_type VARCHAR(100)
);


-- MEDICATIONS

CREATE TABLE indicare.medications (
    encounter_id UUID NOT NULL,
    code VARCHAR(50) NOT NULL,
    start_date DATE,
    stop_date DATE
);

-- PROCEDURES

CREATE TABLE indicare.procedures (
    encounter_id UUID NOT NULL,
    procedure_date DATE,
    code VARCHAR(50) NOT NULL
);

-- ALLERGIES


CREATE TABLE indicare.allergies (
    encounter_id UUID NOT NULL,
    start_date DATE,
    code VARCHAR(50) NOT NULL
);

-- CAREPLANS

CREATE TABLE indicare.careplans (
    careplan_id UUID PRIMARY KEY,
    encounter_id UUID NOT NULL,
    start_date DATE,
    code VARCHAR(50)
);
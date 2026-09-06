-- IndiCare PostgreSQL DDL: constraints.sql
-- Referential Integrity & Validation Constraints (Idempotent)

-- ============================================================
-- 1. FOREIGN KEY CONSTRAINTS
-- ============================================================

-- Encounters -> Patients
ALTER TABLE indicare.encounters DROP CONSTRAINT IF EXISTS fk_encounters_patient;
ALTER TABLE indicare.encounters
    ADD CONSTRAINT fk_encounters_patient
    FOREIGN KEY (patient_id) 
    REFERENCES indicare.patients(patient_id) 
    ON DELETE CASCADE;

-- Careplans -> Patients & Encounters
ALTER TABLE indicare.careplans DROP CONSTRAINT IF EXISTS fk_careplans_patient;
ALTER TABLE indicare.careplans DROP CONSTRAINT IF EXISTS fk_careplans_encounter;
ALTER TABLE indicare.careplans
    ADD CONSTRAINT fk_careplans_patient
    FOREIGN KEY (patient_id) 
    REFERENCES indicare.patients(patient_id) 
    ON DELETE CASCADE,
    ADD CONSTRAINT fk_careplans_encounter
    FOREIGN KEY (encounter_id) 
    REFERENCES indicare.encounters(encounter_id) 
    ON DELETE SET NULL;

-- Conditions -> Patients & Encounters
ALTER TABLE indicare.conditions DROP CONSTRAINT IF EXISTS fk_conditions_patient;
ALTER TABLE indicare.conditions DROP CONSTRAINT IF EXISTS fk_conditions_encounter;
ALTER TABLE indicare.conditions
    ADD CONSTRAINT fk_conditions_patient
    FOREIGN KEY (patient_id) 
    REFERENCES indicare.patients(patient_id) 
    ON DELETE CASCADE,
    ADD CONSTRAINT fk_conditions_encounter
    FOREIGN KEY (encounter_id) 
    REFERENCES indicare.encounters(encounter_id) 
    ON DELETE SET NULL;

-- Observations -> Patients & Encounters
ALTER TABLE indicare.observations DROP CONSTRAINT IF EXISTS fk_observations_patient;
ALTER TABLE indicare.observations DROP CONSTRAINT IF EXISTS fk_observations_encounter;
ALTER TABLE indicare.observations
    ADD CONSTRAINT fk_observations_patient
    FOREIGN KEY (patient_id) 
    REFERENCES indicare.patients(patient_id) 
    ON DELETE CASCADE,
    ADD CONSTRAINT fk_observations_encounter
    FOREIGN KEY (encounter_id) 
    REFERENCES indicare.encounters(encounter_id) 
    ON DELETE SET NULL;

-- Medications -> Patients & Encounters
ALTER TABLE indicare.medications DROP CONSTRAINT IF EXISTS fk_medications_patient;
ALTER TABLE indicare.medications DROP CONSTRAINT IF EXISTS fk_medications_encounter;
ALTER TABLE indicare.medications
    ADD CONSTRAINT fk_medications_patient
    FOREIGN KEY (patient_id) 
    REFERENCES indicare.patients(patient_id) 
    ON DELETE CASCADE,
    ADD CONSTRAINT fk_medications_encounter
    FOREIGN KEY (encounter_id) 
    REFERENCES indicare.encounters(encounter_id) 
    ON DELETE SET NULL;

-- Procedures -> Patients & Encounters
ALTER TABLE indicare.procedures DROP CONSTRAINT IF EXISTS fk_procedures_patient;
ALTER TABLE indicare.procedures DROP CONSTRAINT IF EXISTS fk_procedures_encounter;
ALTER TABLE indicare.procedures
    ADD CONSTRAINT fk_procedures_patient
    FOREIGN KEY (patient_id) 
    REFERENCES indicare.patients(patient_id) 
    ON DELETE CASCADE,
    ADD CONSTRAINT fk_procedures_encounter
    FOREIGN KEY (encounter_id) 
    REFERENCES indicare.encounters(encounter_id) 
    ON DELETE SET NULL;

-- Allergies -> Patients & Encounters
ALTER TABLE indicare.allergies DROP CONSTRAINT IF EXISTS fk_allergies_patient;
ALTER TABLE indicare.allergies DROP CONSTRAINT IF EXISTS fk_allergies_encounter;
ALTER TABLE indicare.allergies
    ADD CONSTRAINT fk_allergies_patient
    FOREIGN KEY (patient_id) 
    REFERENCES indicare.patients(patient_id) 
    ON DELETE CASCADE,
    ADD CONSTRAINT fk_allergies_encounter
    FOREIGN KEY (encounter_id) 
    REFERENCES indicare.encounters(encounter_id) 
    ON DELETE SET NULL;

-- ============================================================
-- 2. CHECK CONSTRAINTS (Chronological Consistency)
-- ============================================================

ALTER TABLE indicare.encounters DROP CONSTRAINT IF EXISTS chk_encounters_stop_time;
ALTER TABLE indicare.encounters
    ADD CONSTRAINT chk_encounters_stop_time
    CHECK (stop_time IS NULL OR stop_time >= start_time);

ALTER TABLE indicare.careplans DROP CONSTRAINT IF EXISTS chk_careplans_stop_time;
ALTER TABLE indicare.careplans
    ADD CONSTRAINT chk_careplans_stop_time
    CHECK (stop_time IS NULL OR stop_time >= start_time);

ALTER TABLE indicare.conditions DROP CONSTRAINT IF EXISTS chk_conditions_stop_date;
ALTER TABLE indicare.conditions
    ADD CONSTRAINT chk_conditions_stop_date
    CHECK (stop_date IS NULL OR stop_date >= start_date);

ALTER TABLE indicare.medications DROP CONSTRAINT IF EXISTS chk_medications_stop_time;
ALTER TABLE indicare.medications
    ADD CONSTRAINT chk_medications_stop_time
    CHECK (stop_time IS NULL OR stop_time >= start_time);

ALTER TABLE indicare.allergies DROP CONSTRAINT IF EXISTS chk_allergies_stop_date;
ALTER TABLE indicare.allergies
    ADD CONSTRAINT chk_allergies_stop_date
    CHECK (stop_date IS NULL OR stop_date >= start_date);

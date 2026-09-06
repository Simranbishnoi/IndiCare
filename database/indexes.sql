-- IndiCare PostgreSQL DDL: indexes.sql
-- Performance Optimization Indexes for Foreign Keys & Cohort Queries

-- ============================================================
-- 1. FOREIGN KEY INDEXES (Accelerates JOINS across tables)
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_encounters_patient_id ON indicare.encounters(patient_id);
CREATE INDEX IF NOT EXISTS idx_careplans_patient_id ON indicare.careplans(patient_id);
CREATE INDEX IF NOT EXISTS idx_careplans_encounter_id ON indicare.careplans(encounter_id);
CREATE INDEX IF NOT EXISTS idx_conditions_patient_id ON indicare.conditions(patient_id);
CREATE INDEX IF NOT EXISTS idx_conditions_encounter_id ON indicare.conditions(encounter_id);
CREATE INDEX IF NOT EXISTS idx_observations_patient_id ON indicare.observations(patient_id);
CREATE INDEX IF NOT EXISTS idx_observations_encounter_id ON indicare.observations(encounter_id);
CREATE INDEX IF NOT EXISTS idx_medications_patient_id ON indicare.medications(patient_id);
CREATE INDEX IF NOT EXISTS idx_medications_encounter_id ON indicare.medications(encounter_id);
CREATE INDEX IF NOT EXISTS idx_procedures_patient_id ON indicare.procedures(patient_id);
CREATE INDEX IF NOT EXISTS idx_procedures_encounter_id ON indicare.procedures(encounter_id);
CREATE INDEX IF NOT EXISTS idx_allergies_patient_id ON indicare.allergies(patient_id);
CREATE INDEX IF NOT EXISTS idx_allergies_encounter_id ON indicare.allergies(encounter_id);

-- ============================================================
-- 2. COHORT SELECTION INDEXES (Accelerates clinical filtering)
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_conditions_code ON indicare.conditions(code);
CREATE INDEX IF NOT EXISTS idx_observations_code ON indicare.observations(code);
CREATE INDEX IF NOT EXISTS idx_medications_code ON indicare.medications(code);
CREATE INDEX IF NOT EXISTS idx_procedures_code ON indicare.procedures(code);
CREATE INDEX IF NOT EXISTS idx_allergies_code ON indicare.allergies(code);

-- Composite Index for temporal cohort queries
CREATE INDEX IF NOT EXISTS idx_observations_patient_code ON indicare.observations(patient_id, code);
CREATE INDEX IF NOT EXISTS idx_conditions_patient_code ON indicare.conditions(patient_id, code);

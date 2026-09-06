-- IndiCare PostgreSQL DDL: views.sql
-- Analytical & Cohort Selection Views

-- 1. Patient Summary View
CREATE OR REPLACE VIEW indicare.vw_patient_summary AS
SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS full_name,
    p.gender,
    p.birth_date,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.birth_date)) AS age,
    p.marital_status,
    p.race,
    p.ethnicity,
    COUNT(DISTINCT e.encounter_id) AS total_encounters,
    COUNT(DISTINCT c.condition_id) AS total_conditions
FROM indicare.patients p
LEFT JOIN indicare.encounters e ON p.patient_id = e.patient_id
LEFT JOIN indicare.conditions c ON p.patient_id = c.patient_id
GROUP BY p.patient_id, full_name, p.gender, p.birth_date, p.marital_status, p.race, p.ethnicity;

-- 2. Heart Disease Cohort View (For ML Layer)
CREATE OR REPLACE VIEW indicare.vw_cohort_heart_disease AS
SELECT DISTINCT
    p.patient_id,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.birth_date)) AS age,
    p.gender,
    p.race,
    c.code AS condition_code,
    c.description AS condition_name,
    c.start_date AS diagnosed_date
FROM indicare.patients p
JOIN indicare.conditions c ON p.patient_id = c.patient_id
WHERE LOWER(c.description) LIKE '%heart%' 
   OR LOWER(c.description) LIKE '%cardiac%'
   OR LOWER(c.description) LIKE '%hypertension%';

-- 3. Encounter Metrics View
CREATE OR REPLACE VIEW indicare.vw_encounter_metrics AS
SELECT 
    e.encounter_id,
    e.patient_id,
    e.encounter_class,
    e.start_time,
    e.stop_time,
    EXTRACT(EPOCH FROM (e.stop_time - e.start_time))/3600 AS duration_hours,
    COUNT(DISTINCT pr.procedure_id) AS procedure_count,
    COUNT(DISTINCT m.medication_id) AS medication_count
FROM indicare.encounters e
LEFT JOIN indicare.procedures pr ON e.encounter_id = pr.encounter_id
LEFT JOIN indicare.medications m ON e.encounter_id = m.encounter_id
GROUP BY e.encounter_id, e.patient_id, e.encounter_class, e.start_time, e.stop_time;

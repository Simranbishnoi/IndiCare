-- IndiCare Relational Algebra: joins.sql
-- Join Operator (bowtie): Combines patients, encounters, and conditions

SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    e.encounter_id,
    e.start_time AS visit_date,
    c.description AS condition_diagnosed
FROM indicare.patients p
JOIN indicare.encounters e ON p.patient_id = e.patient_id
JOIN indicare.conditions c ON e.encounter_id = c.encounter_id;

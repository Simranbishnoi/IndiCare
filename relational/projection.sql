-- IndiCare Relational Algebra: projection.sql
-- Projection Operator (pi): Selects specific column attributes

SELECT 
    patient_id, 
    first_name, 
    last_name, 
    gender, 
    race 
FROM indicare.patients;

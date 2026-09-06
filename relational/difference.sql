-- IndiCare Relational Algebra: difference.sql
-- Difference Operator (-): Patients with hypertension EXCEPT those with diabetes

SELECT patient_id FROM indicare.conditions WHERE LOWER(description) LIKE '%hypertension%'
EXCEPT
SELECT patient_id FROM indicare.conditions WHERE LOWER(description) LIKE '%diabetes%';

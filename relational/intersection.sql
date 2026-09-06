-- IndiCare Relational Algebra: intersection.sql
-- Intersection Operator (cap): Finds patients with BOTH hypertension AND diabetes

SELECT patient_id FROM indicare.conditions WHERE LOWER(description) LIKE '%hypertension%'
INTERSECT
SELECT patient_id FROM indicare.conditions WHERE LOWER(description) LIKE '%diabetes%';

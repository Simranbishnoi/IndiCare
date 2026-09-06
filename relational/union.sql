-- IndiCare Relational Algebra: union.sql
-- Union Operator (cup): Combines unique patients with hypertension OR diabetes

SELECT patient_id FROM indicare.conditions WHERE LOWER(description) LIKE '%hypertension%'
UNION
SELECT patient_id FROM indicare.conditions WHERE LOWER(description) LIKE '%diabetes%';

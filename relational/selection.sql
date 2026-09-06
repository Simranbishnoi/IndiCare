-- IndiCare Relational Algebra: selection.sql
-- Selection Operator (sigma): Filters rows based on condition predicate

SELECT * 
FROM indicare.patients 
WHERE gender = 'M' 
  AND birth_date >= '1970-01-01';

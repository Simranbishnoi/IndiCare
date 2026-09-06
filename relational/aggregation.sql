-- IndiCare Relational Algebra: aggregation.sql
-- Aggregation Operator (gamma): Grouping and summary calculations

SELECT 
    p.gender,
    p.race,
    COUNT(DISTINCT p.patient_id) AS patient_count,
    ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.birth_date))), 1) AS avg_age
FROM indicare.patients p
GROUP BY p.gender, p.race;

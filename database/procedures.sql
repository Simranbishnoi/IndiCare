-- IndiCare PostgreSQL DDL: procedures.sql
-- Automated Staging to Relational Migration Procedure

CREATE OR REPLACE PROCEDURE indicare.migrate_staging_to_relational()
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Starting migration from Staging to Relational tables...';

    -- 1. Migrate Patients
    INSERT INTO indicare.patients (
        patient_id, first_name, last_name, birth_date, death_date,
        marital_status, race, ethnicity, gender, county, fips, zip, lat, lon
    )
    SELECT DISTINCT
        id, first, last, birthdate, deathdate,
        marital, race, ethnicity, gender, county, fips, zip, lat, lon
    FROM indicare.stg_patients
    ON CONFLICT (patient_id) DO NOTHING;

    -- 2. Migrate Encounters
    INSERT INTO indicare.encounters (
        encounter_id, start_time, stop_time, patient_id,
        organization_id, provider_id, payer_id, encounter_class, code, reason_code, reason_description
    )
    SELECT DISTINCT
        e.id, e.start_time, e.stop_time, e.patient_id,
        e.organization, e.provider, e.payer, e.encounterclass, e.code, e.reasoncode, e.reasondescription
    FROM indicare.stg_encounters e
    JOIN indicare.patients p ON e.patient_id = p.patient_id
    ON CONFLICT (encounter_id) DO NOTHING;

    -- 3. Migrate Careplans (Orphan encounter safe)
    INSERT INTO indicare.careplans (
        careplan_id, start_time, stop_time, patient_id, encounter_id, code, description, reason_code, reason_description
    )
    SELECT DISTINCT
        c.id, c.start_time, c.stop_time, c.patient_id,
        e.encounter_id, c.code, c.description, c.reasoncode, c.reasondescription
    FROM indicare.stg_careplans c
    JOIN indicare.patients p ON c.patient_id = p.patient_id
    LEFT JOIN indicare.encounters e ON c.encounter_id = e.encounter_id
    ON CONFLICT (careplan_id) DO NOTHING;

    -- 4. Migrate Conditions (Orphan encounter safe)
    INSERT INTO indicare.conditions (
        start_date, stop_date, patient_id, encounter_id, system, code, description
    )
    SELECT
        c.start_date, c.stop_date, c.patient_id,
        e.encounter_id, c.system, c.code, c.description
    FROM indicare.stg_conditions c
    JOIN indicare.patients p ON c.patient_id = p.patient_id
    LEFT JOIN indicare.encounters e ON c.encounter_id = e.encounter_id;

    -- 5. Migrate Observations (Orphan encounter safe)
    INSERT INTO indicare.observations (
        obs_date, patient_id, encounter_id, category, code, description, value, units, obs_type
    )
    SELECT
        o.obs_date, o.patient_id,
        e.encounter_id, o.category, o.code, o.description, o.value, o.units, o.obs_type
    FROM indicare.stg_observations o
    JOIN indicare.patients p ON o.patient_id = p.patient_id
    LEFT JOIN indicare.encounters e ON o.encounter_id = e.encounter_id;

    -- 6. Migrate Medications (Orphan encounter safe)
    INSERT INTO indicare.medications (
        start_time, stop_time, patient_id, payer_id, encounter_id, code, description,
        base_cost, payer_coverage, dispenses, total_cost, reason_code, reason_description
    )
    SELECT
        m.start_time, m.stop_time, m.patient_id, m.payer_id,
        e.encounter_id, m.code, m.description, m.base_cost, m.payer_coverage, m.dispenses, m.total_cost, m.reasoncode, m.reasondescription
    FROM indicare.stg_medications m
    JOIN indicare.patients p ON m.patient_id = p.patient_id
    LEFT JOIN indicare.encounters e ON m.encounter_id = e.encounter_id;

    -- 7. Migrate Procedures (Orphan encounter safe)
    INSERT INTO indicare.procedures (
        start_time, stop_time, patient_id, encounter_id, system, code, description, base_cost, reason_code, reason_description
    )
    SELECT
        pr.start_time, pr.stop_time, pr.patient_id,
        e.encounter_id, pr.system, pr.code, pr.description, pr.base_cost, pr.reasoncode, pr.reasondescription
    FROM indicare.stg_procedures pr
    JOIN indicare.patients p ON pr.patient_id = p.patient_id
    LEFT JOIN indicare.encounters e ON pr.encounter_id = e.encounter_id;

    -- 8. Migrate Allergies (Orphan encounter safe)
    INSERT INTO indicare.allergies (
        start_date, stop_date, patient_id, encounter_id, code, system, description, type, category,
        reaction1, description1, severity1, reaction2, description2, severity2
    )
    SELECT
        a.start_date, a.stop_date, a.patient_id,
        e.encounter_id, a.code, a.system, a.description, a.type, a.category,
        a.reaction1, a.description1, a.severity1, a.reaction2, a.description2, a.severity2
    FROM indicare.stg_allergies a
    JOIN indicare.patients p ON a.patient_id = p.patient_id
    LEFT JOIN indicare.encounters e ON a.encounter_id = e.encounter_id;

    RAISE NOTICE 'Migration successfully completed!';
END;
$$;

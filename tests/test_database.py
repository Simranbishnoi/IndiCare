import os
import pytest
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "indicare")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

@pytest.fixture(scope="module")
def db_conn():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        yield conn
        conn.close()
    except Exception:
        pytest.skip("Database connection not available for test execution")

def test_schema_exists(db_conn):
    cur = db_conn.cursor()
    cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'indicare';")
    schema = cur.fetchone()
    assert schema is not None, "Schema 'indicare' does not exist"

def test_tables_exist(db_conn):
    cur = db_conn.cursor()
    expected_tables = [
        "patients", "encounters", "careplans", "conditions",
        "observations", "medications", "procedures", "allergies"
    ]
    for table in expected_tables:
        cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'indicare' AND table_name = '{table}';")
        res = cur.fetchone()
        assert res is not None, f"Table 'indicare.{table}' does not exist"

def test_views_exist(db_conn):
    cur = db_conn.cursor()
    expected_views = ["vw_patient_summary", "vw_cohort_heart_disease", "vw_encounter_metrics"]
    for view in expected_views:
        cur.execute(f"SELECT table_name FROM information_schema.views WHERE table_schema = 'indicare' AND table_name = '{view}';")
        res = cur.fetchone()
        assert res is not None, f"View 'indicare.{view}' does not exist"

def test_audit_table_exists(db_conn):
    cur = db_conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'indicare' AND table_name = 'audit_log';")
    res = cur.fetchone()
    assert res is not None, "Audit log table 'indicare.audit_log' does not exist"

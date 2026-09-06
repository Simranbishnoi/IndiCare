import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "indicare")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

def ensure_database_exists():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()
        if not exists:
            print(f"Database '{DB_NAME}' does not exist. Creating database '{DB_NAME}'...")
            cur.execute(f'CREATE DATABASE "{DB_NAME}";')
            print(f"Database '{DB_NAME}' successfully created!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Note on DB creation: {e}")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def execute_sql_file(cursor, filepath):
    print(f"Executing: {os.path.basename(filepath)}...")
    with open(filepath, "r", encoding="utf-8") as f:
        cursor.execute(f.read())

def copy_csv_to_staging(cursor, table_name, csv_filename):
    csv_path = os.path.join(DATA_DIR, csv_filename)
    if not os.path.exists(csv_path):
        print(f"Skipping {csv_filename} (file not found at {csv_path})")
        return
    print(f"Bulk loading {csv_filename} -> {table_name}...")
    with open(csv_path, "r", encoding="utf-8") as f:
        # Skip header line
        next(f)
        cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH (FORMAT csv, HEADER false)", f)

def run_pipeline():
    ensure_database_exists()
    
    conn = get_connection()
    conn.autocommit = False
    cur = conn.cursor()
    try:
        # 1. Initialize Schema and Tables
        execute_sql_file(cur, os.path.join(DB_DIR, "schema.sql"))
        execute_sql_file(cur, os.path.join(DB_DIR, "tables.sql"))
        execute_sql_file(cur, os.path.join(DB_DIR, "procedures.sql"))

        # 2. Bulk Load Processed CSVs into Staging
        copy_csv_to_staging(cur, "indicare.stg_patients", "patients_processed.csv")
        copy_csv_to_staging(cur, "indicare.stg_encounters", "encounters_processed.csv")
        copy_csv_to_staging(cur, "indicare.stg_careplans", "careplans_processed.csv")
        copy_csv_to_staging(cur, "indicare.stg_conditions", "conditions_processed.csv")
        copy_csv_to_staging(cur, "indicare.stg_observations", "observations_processed.csv")
        copy_csv_to_staging(cur, "indicare.stg_medications", "medications_processed.csv")
        copy_csv_to_staging(cur, "indicare.stg_procedures", "procedures_processed.csv")
        copy_csv_to_staging(cur, "indicare.stg_allergies", "allergies_processed.csv")

        # 3. Migrate Staging to Final Relational Tables
        print("Migrating Staging Data -> Final Relational Tables...")
        cur.execute("CALL indicare.migrate_staging_to_relational();")

        # 4. Apply Constraints, Indexes, Views, and Audit
        execute_sql_file(cur, os.path.join(DB_DIR, "constraints.sql"))
        execute_sql_file(cur, os.path.join(DB_DIR, "indexes.sql"))
        execute_sql_file(cur, os.path.join(DB_DIR, "views.sql"))
        execute_sql_file(cur, os.path.join(DB_DIR, "audit.sql"))

        conn.commit()
        print("\n🎉 SUCCESS! PostgreSQL Database Pipeline Successfully Completed!")
    except Exception as e:
        conn.rollback()
        print(f"Error executing database pipeline: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_pipeline()

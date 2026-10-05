import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_unified_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='KANISHAJAI2007',
            host='127.0.0.1',
            port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname='hospital_management_system'")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE hospital_management_system;")
            print("Database 'hospital_management_system' created successfully.")
        else:
            print("Database 'hospital_management_system' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_unified_database()
